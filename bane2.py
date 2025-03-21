import pygame
import random
import math
from constants import *
# landskab klasse


class Bane:
    """
    Bane klassen håndterer spillets verden og terræn.
    Indeholder metoder til at tegne og opdatere spillets miljø.
    """
    
    def __init__(self, width, height):
        """
        Konstruktør for Bane klassen.
        
        Parametre:
            width (int): Skærmens bredde i pixels
            height (int): Skærmens højde i pixels
        """
        # Gem banens dimensioner som attributter
        self.width = width  # Bredde af banen
        self.height = height  # Højde af banen
        
        platform_width = width * 0.7  # Platform 70% af width
        platform_x = (width - platform_width) / 2  # Center the platform
        platform_y = height * 0.75  # Platform 75% height
        self.platform_segments = [
            pygame.Rect(platform_x, platform_y, platform_width, 20)  # 
        ]
        
        # Void under platform
        self.void_y = platform_y + 30  # Start void a bit below platform
        
        # 
        self.tree_positions = [
            {"x": self.width * 0.18, "health": 1.0},  # venstre træ
            
            {"x": self.width * 0.82, "health": 1.0}   # højre træ
        ]
        
        # Farvetemaer for dag og nat gamel kode
        self.color_themes = {
            "day": {
                "background": (135, 206, 235),  # Lyseblå himmel
                "mountain": (101, 67, 33),  # Brun bjerg
                "ground": (34, 139, 34),  # Grøn jord
                "platform": (139, 69, 19)  # Brun platform
            },
            "night": {
                "background": (25, 25, 112),  # Mørkeblå nattehimmel
                "mountain": (72, 61, 139),  # Mørklilla bjerg
                "ground": (0, 100, 0),  # Mørkegrøn jord
                "platform": (85, 45, 10)  # Mørkebrun platform
            }
        }
        
        # Aktuelle farvetema (starter med dag)
        self.current_theme = "day"
        
        # Tid for sidste temaændring
        self.last_theme_change = 0
        
        # Interval for temaændring i millisekunder (10 sekunder)
        self.theme_change_interval = 10000

    # Hent de aktuelle farver baseret på temaet
    def get_current_colors(self):
        """
        Henter det aktuelle farvetemas farver.
        
        Returværdi:
            dict: Dictionary med de aktuelle temafarver
        """
        # Returner farverne for det aktuelle tema
        return self.color_themes[self.current_theme]

    # Opdater banen (f.eks. skift mellem dag og nat)
    def update(self, current_time):
        """
        Opdaterer banens tilstand.
        
        Parametre:
            current_time (int): Nuværende spilletid i millisekunder
        """
        # Tjek om det er tid til at skifte tema
        if current_time - self.last_theme_change > self.theme_change_interval:
            # Skift mellem dag og nat
            self.current_theme = "night" if self.current_theme == "day" else "day"
            # Opdater tidspunkt for sidste ændring
            self.last_theme_change = current_time

    # Tegn banen med alle elementer 
    def draw(self, surface: pygame.Surface, spiller1=None, spiller2=None):
        """
        Tegner hele banen med alle elementer.
        
        Parametre:
            surface (pygame.Surface): Overfladen der skal tegnes på
            spiller1 (Spiller): Første spiller objekt, bruges til skadevisning
            spiller2 (Spiller): Anden spiller objekt, bruges til skadevisning
        """
        # Opret gradient baggrund
        for y in range(self.height):
            # Beregn gradientværdi baseret på y-position
            gradient_value = max(0, min(50 + y // 2, 80))
            pygame.draw.line(surface, (gradient_value//2, gradient_value//2, gradient_value), 
                          (0, y), (self.width, y))
        
        # Tegn afgrunden under platformen
        void_rect = pygame.Rect(0, self.void_y, self.width, self.height - self.void_y)
        pygame.draw.rect(surface, (10, 10, 15), void_rect)
        
        # Tilføj partikkeleffekter i afgrunden
        for _ in range(20):
            particle_x = random.randint(0, self.width)
            particle_y = random.randint(int(self.void_y), self.height)
            particle_size = random.randint(1, 3)
            particle_color = (30, 30, 40)
            pygame.draw.circle(surface, particle_color, (particle_x, particle_y), particle_size)
        
        # Definér og tegn baggrundsbjerge
        hill_color = (30, 40, 45)  # Mørk blågrøn farve til fjerne bjerge
        hills = [
            # Venstre bjergkæde
            [(0, self.height * 0.6), 
             (self.width * 0.15, self.height * 0.55), 
             (self.width * 0.35, self.height * 0.58), 
             (self.width * 0.4, self.height * 0.6)],
            # Højre bjergkæde
            [(self.width * 0.6, self.height * 0.6), 
             (self.width * 0.7, self.height * 0.57), 
             (self.width * 0.9, self.height * 0.59), 
             (self.width, self.height * 0.58), 
             (self.width, self.height * 0.65)]
        ]
        
        # Tegn bjergkæderne
        for hill in hills:
            pygame.draw.polygon(surface, hill_color, hill)
        
        # Tegn Mount Fuji i centrum
        self._draw_mount_fuji(surface)
        
        # Opdater og tegn kirsebærtræer med spillernes skadeprocent
        left_damage = spiller1.damage if spiller1 else 0
        right_damage = spiller2.damage if spiller2 else 0
        
        # Tegn træerne på hver side
        self.draw_cherry_tree(
            self.tree_positions[0]["x"],
            self.height,
            self.tree_positions[0]["health"],
            skadeprocent=left_damage,
            surface=surface
        )
        
        self.draw_cherry_tree(
            self.tree_positions[1]["x"],
            self.height,
            self.tree_positions[1]["health"],
            skadeprocent=right_damage,
            surface=surface
        )
        
        # Tegn torii-porten (traditionel japansk portal)
        self._draw_torii(surface)
        
        # Tegn terræn og platform
        self._draw_terrain(surface)
        self._draw_platforms(surface)

    def _draw_mount_fuji(self, surface):
        """
        Hjælpemetode til at tegne Mount Fuji.
        
        Parametre:
            surface (pygame.Surface): Overfladen der skal tegnes på
        """
        # Definér bjergets basepunkter
        mountain_base = [
            (self.width * 0.5, self.height * 0.2),    # Toppunkt
            (self.width * 0.46, self.height * 0.25),  # Højre øvre kurve
            (self.width * 0.42, self.height * 0.28),  # Højre skulder
            (self.width * 0.36, self.height * 0.35),  # Højre skråning
            (self.width * 0.28, self.height * 0.45),  # Højre midterskråning
            (self.width * 0.2, self.height * 0.55),   # Højre nedre skråning
            (self.width * 0.12, self.height * 0.7),   # Højre base
            (self.width * 0.88, self.height * 0.7),   # Venstre base
            (self.width * 0.8, self.height * 0.55),   # Venstre nedre skråning
            (self.width * 0.72, self.height * 0.45),  # Venstre midterskråning
            (self.width * 0.64, self.height * 0.35),  # Venstre skråning
            (self.width * 0.58, self.height * 0.28),  # Venstre skulder
            (self.width * 0.54, self.height * 0.25),  # Venstre øvre kurve
        ]
        
        # Tegn bjergets base
        pygame.draw.polygon(surface, (60, 50, 55), mountain_base)
        
        # Definér og tegn snedækket
        snow_cap = [
            (self.width * 0.5, self.height * 0.2),    # Toppunkt
            (self.width * 0.46, self.height * 0.25),  # Højre øvre kant
            (self.width * 0.42, self.height * 0.28),  # Højre skulder
            (self.width * 0.39, self.height * 0.31),  # Højre snekant 1
            (self.width * 0.37, self.height * 0.32),  # Højre snepunkt 1
            (self.width * 0.35, self.height * 0.33),  # Højre snekant 2
            (self.width * 0.33, self.height * 0.34),  # Højre snepunkt 2
            (self.width * 0.31, self.height * 0.39),  # Højre snekant 3
            (self.width * 0.29, self.height * 0.4),   # Højre snekurve
            (self.width * 0.28, self.height * 0.41),  # Højre sneafslutning
            (self.width * 0.72, self.height * 0.41),  # Venstre sneafslutning
            (self.width * 0.71, self.height * 0.4),   # Venstre snekurve
            (self.width * 0.69, self.height * 0.39),  # Venstre snekant 3
            (self.width * 0.67, self.height * 0.34),  # Venstre snepunkt 2
            (self.width * 0.65, self.height * 0.33),  # Venstre snekant 2
            (self.width * 0.63, self.height * 0.32),  # Venstre snepunkt 1
            (self.width * 0.61, self.height * 0.31),  # Venstre snekant 1
            (self.width * 0.58, self.height * 0.28),  # Venstre skulder
            (self.width * 0.54, self.height * 0.25),  # Venstre øvre kant
        ]
        
        # Tegn snedækket
        pygame.draw.polygon(surface, (240, 240, 240), snow_cap)

    def _draw_torii(self, surface):
        """
        Hjælpemetode til at tegne torii-porten.
        
        Parametre:
            surface (pygame.Surface): Overfladen der skal tegnes på
        """
        # Definér torii-portens dimensioner
        torii_color = (180, 40, 40)  # Traditionel rød farve
        torii_x = self.width * 0.5   # Centrér porten
        torii_y = self.height * 0.65  # Portens højdeplacering
        torii_width = self.width * 0.15
        torii_height = self.height * 0.1
        
        # Tegn søjlerne
        pygame.draw.rect(surface, torii_color, 
                      (torii_x - torii_width/2, torii_y, 
                       torii_width * 0.1, torii_height))
        pygame.draw.rect(surface, torii_color, 
                      (torii_x + torii_width/2 - torii_width * 0.1, torii_y, 
                       torii_width * 0.1, torii_height))
        
        # Tegn tværbjælkerne
        pygame.draw.rect(surface, torii_color, 
                      (torii_x - torii_width/2 - torii_width * 0.05, 
                       torii_y, torii_width * 1.1, torii_height * 0.15))
        pygame.draw.rect(surface, torii_color, 
                      (torii_x - torii_width/2, torii_y + torii_height * 0.25, 
                       torii_width, torii_height * 0.1))

    def _draw_terrain(self, surface):
        """
        Hjælpemetode til at tegne terrænet.
        
        Parametre:
            surface (pygame.Surface): Overfladen der skal tegnes på
        """
        # Tegn jordoverfladen
        ground_rect = pygame.Rect(0, self.height * 0.7, self.width, self.height * 0.3)
        pygame.draw.rect(surface, (40, 50, 40), ground_rect)
        
        # Tilføj græsstrå for tekstur
        for _ in range(100):
            grass_x = random.randint(0, self.width)
            grass_height = random.randint(2, 5)
            pygame.draw.line(surface, (50, 70, 50), 
                          (grass_x, self.height * 0.7), 
                          (grass_x, self.height * 0.7 - grass_height))

    def _draw_platforms(self, surface):
        """
        Hjælpemetode til at tegne platforme.
        
        Parametre:
            surface (pygame.Surface): Overfladen der skal tegnes på
        """
        for platform in self.platform_segments:
            # Tegn hovedplatformen
            pygame.draw.rect(surface, (120, 80, 40), platform)
            
            # Tilføj dekorative træårer
            line_spacing = 20
            for y in range(platform.top, platform.bottom, line_spacing):
                pygame.draw.line(surface, (90, 60, 30),
                               (platform.left, y),
                               (platform.right, y), 2)
            
            # Tilføj platformkanter
            pygame.draw.rect(surface, (90, 60, 30), platform, 4)
            
            # Tilføj traditionelle endestykker
            cap_width = 8
            pygame.draw.rect(surface, (140, 90, 40), 
                          (platform.left - cap_width//2, platform.top - 5,
                           platform.width + cap_width, 10))
            
            # Tilføj skyggeeffekter
            pygame.draw.rect(surface, (80, 50, 25), 
                           (platform.left, platform.bottom, platform.width, 3))
            pygame.draw.rect(surface, (100, 65, 35), 
                           (platform.left - 2, platform.top, 2, platform.height))
            pygame.draw.rect(surface, (100, 65, 35), 
                           (platform.right, platform.top, 2, platform.height))

    def is_on_platform(self, x, y):
        """
        Tjekker om en given position er på en platform.
        
        Parametre:
            x (float): X-koordinat at tjekke
            y (float): Y-koordinat at tjekke
            
        Returværdi:
            bool: Sand hvis positionen er på en platform, ellers falsk
        """
        for platform in self.platform_segments:
            if (platform.left <= x <= platform.right and
                platform.top <= y <= platform.bottom):
                return True
        return False

    def get_platform_y(self, x):
        """
        Finder y-koordinaten for den øverste platform ved en given x-koordinat.
        
        Parametre:
            x (float): X-koordinat at tjekke
            
        Returværdi:
            float eller None: Y-koordinat for platformen, eller None hvis ingen platform findes
        """
        min_y = float('inf')
        for platform in self.platform_segments:
            if platform.left <= x <= platform.right:
                min_y = min(min_y, platform.top)
        return min_y if min_y != float('inf') else None

    def handle_input(self):
        # Remove this method or leave it empty
        pass

    def draw_cherry_tree(self, x, height, health, skadeprocent=0, flip=False, surface=None):
        if surface is None:
            return
            
        # Beregn træets højde baseret på skadeprocent
        # Jo højere skade, jo højere bliver træet
        # Vi starter med normal højde og tilføjer ekstra højde baseret på skade
        base_height = self.height * 0.15  # Normal højde
        extra_height = (skadeprocent / 100) * (self.height * 0.2)  # Ekstra højde baseret på skade
        total_height = base_height + extra_height
        
        # Træstamme - mørkere og mere defineret
        trunk_width = self.width * 0.025  # Bredden af stammen
        
        # Lav træstammen
        trunk = pygame.Rect(
            x - trunk_width // 2,  # Centrer stammen på x-positionen
            self.height * 0.7 - total_height,  # Start fra bunden og gå op
            trunk_width,
            total_height
        )
        
        # Tegn stammen med mørkebrun farve og outline
        pygame.draw.rect(surface, (45, 30, 20), trunk)  # Indre del af stammen
        pygame.draw.rect(surface, (35, 20, 15), trunk, 2)  # Outline af stammen
        
        # Beregn bladenes position og størrelse
        # Bladene skal sidde i toppen af træet
        foliage_center_y = self.height * 0.7 - total_height - self.height * 0.08
        
        # Størrelsen af bladene afhænger også lidt af skaden
        foliage_radius = self.width * 0.06 * health * (1 + skadeprocent/200)
        
        # Positioner for de forskellige dele af bladene
        # Vi laver flere cirkler der overlapper for at lave en pæn trækrone
        foliage_positions = [
            (x, foliage_center_y),  # Midten
            (x - foliage_radius * 0.7, foliage_center_y + foliage_radius * 0.3),  # Venstre
            (x + foliage_radius * 0.7, foliage_center_y + foliage_radius * 0.3),  # Højre
            (x, foliage_center_y + foliage_radius * 0.5),  # Bund
            (x, foliage_center_y - foliage_radius * 0.5),  # Top
        ]
        
        # Beregn farver baseret på skade
        # Jo mere skade, jo mere rødlig bliver træet
        damage_factor = 1 - health
        base_color = (
            min(255, 200 + int(damage_factor * 55)),  # Mere rød ved skade
            max(0, 100 - int(damage_factor * 100)),   # Mindre grøn ved skade
            max(0, 150 - int(damage_factor * 150))    # Mindre blå ved skade
        )
        
        # Tegn alle blade
        for pos_x, pos_y in foliage_positions:
            pygame.draw.circle(surface, base_color, (int(pos_x), int(pos_y)), int(foliage_radius))