import pygame

import random
import math

from constants import *

# landskab klasse


class Bane:
    """

        Bane klassen håndterer spillets verden og terræn.
    Denne klasse er ansvarlig for at:
    - Oprette og vedligeholde spillets platform
    - Tegne baggrunden med Mount Fuji
    - Håndtere træer og deres tilstand
    - Tegne en rød port
    """
    
    def __init__(self, width, height):
        """
        Initialiserer en ny bane med de givne dimensioner.
        
        Parametre:
            width (int): Skærmens bredde i pixels
            height (int): Skærmens højde i pixels
    
            """
        # Gem banens dimensioner som attributter
    
        self.width = width   # Gemmer skærmens bredde
    
        self.height = height # Gemmer skærmens højde
        
        # Beregn platformens dimensioner og position
    
        platformBredde = width * 0.7  # Sætter platformens bredde til 70% af skærmbredden
    
        platformX = (width - platformBredde) / 2  # Centrerer platformen vandret
        platformY = height * 0.75  # Placerer platformen 75% nede på skærmen


        # Opret platform segmenter som rektangler
        self.platformSegments = [
    
            pygame.Rect(platformX, platformY, platformBredde, 20)  # Hovedplatform med 20 pixels højde
        ]


        # Definer afgrunden under platformen
        self.voidY = platformY + 30  # Starter afgrunden 30 pixels under platformen
        
    
        # Definer positioner for kirsebærtræerne
        self.trePositions = [
    
            {"x": self.width * 0.18, "health": 1.0},  # Venstre træ placeret 18% inde fra venstre
    
            {"x": self.width * 0.82, "health": 1.0}   # Højre træ placeret 82% inde fra venstre
        ]

    
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
        voidRect = pygame.Rect(0, self.voidY, self.width, self.height - self.voidY)
        
        pygame.draw.rect(surface, (10, 10, 15), voidRect)
        
        # Tilføj partikkeleffekter i afgrunden
        
        for _ in range(20):
            particleX = random.randint(0, self.width)
        
            particleY = random.randint(int(self.voidY), self.height)
            particleSize = random.randint(1, 3)
        
            particleColor = (30, 30, 40)
            pygame.draw.circle(surface, particleColor, (particleX, particleY), particleSize)
        

        
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
        
        self.drawMountFuji(surface)
        

        
        # Opdater og tegn kirsebærtræer med spillernes skadeprocent
        
        leftDamage = spiller1.damage if spiller1 else 0
        rightDamage = spiller2.damage if spiller2 else 0
        

        # Tegn træerne på hver side
        self.drawCherryTree(
        
            self.trePositions[0]["x"],
            self.height,
        
            self.trePositions[0]["health"],
            skadeprocent=leftDamage,
        
            surface=surface
        )
        
        self.drawCherryTree(
        
            self.trePositions[1]["x"],
        
            self.height,
            self.trePositions[1]["health"],
        
            skadeprocent=rightDamage,
            surface=surface
        
        )
        
        # Tegn torii-porten (traditionel japansk portal)
        
        self.drawTorii(surface)
        

        # Tegn terræn og platform
        
        self.drawTerrain(surface)
        self.drawPlatforms(surface)

    def drawMountFuji(self, surface):
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


    def drawTorii(self, surface):
        """
        Hjælpemetode til at tegne torii-porten.
        
        Parametre:
            surface (pygame.Surface): Overfladen der skal tegnes på
        """
        # Definer torii portens dimensioner

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


    def drawTerrain(self, surface):
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

    def drawPlatforms(self, surface):
        """

                Hjælpemetode til at tegne platforme.
        
        Parametre:
            surface (pygame.Surface): Overfladen der skal tegnes på
        """
        for platform in self.platformSegments:
            # Tegn hovedplatformen
            pygame.draw.rect(surface, (120, 80, 40), platform)
            
            # Tilføj dekorative træårer
            lineSpacing = 20
        
            for y in range(platform.top, platform.bottom, lineSpacing):
        
                pygame.draw.line(surface, (90, 60, 30),
                               (platform.left, y),
        
                               (platform.right, y), 2)


        
            # Tilføj platformkanter
            capBredde = 8
        
        
            pygame.draw.rect(surface, (140, 90, 40), 
                          (platform.left - capBredde//2, platform.top - 5,
        
                           platform.width + capBredde, 10))
            
            # Tilføj skyggeeffekter
            pygame.draw.rect(surface, (80, 50, 25), 
        
                           (platform.left, platform.bottom, platform.width, 3))
            pygame.draw.rect(surface, (100, 65, 35), 
        
                           (platform.left - 2, platform.top, 2, platform.height))
        
            pygame.draw.rect(surface, (100, 65, 35), 
                           (platform.right, platform.top, 2, platform.height))


    def isOnPlatform(self, x, y):
        """Tjekker om en given position er på en platform."""

        for platform in self.platformSegments:
            if (platform.left <= x <= platform.right and

                platform.top <= y <= platform.bottom):

                return True

        return False

    def getPlatformY(self, x):
        """Finder y koordinaten for den øverste platform ved en given x koordinat."""

        minY = float('inf')

        for platform in self.platformSegments:

            if platform.left <= x <= platform.right:

                minY = min(minY, platform.top)

        return minY if minY != float('inf') else None


    def handleInput(self):
        pass

    def drawCherryTree(self, x, height, health, skadeprocent=0, flip=False, surface=None):

        if surface is None:
            return
            

        # Beregn træets højde baseret på skadeprocent
        baseHeight = self.height * 0.15  # Normal højde

        extraHeight = (skadeprocent / 100) * (self.height * 0.2)  # Ekstra højde baseret på skade

        totalHeight = baseHeight + extraHeight


        # Træstamme - mørkere og mere defineret
        trunkBredde = self.width * 0.025  # Bredden af stammen
        
        # Lav træstammen
        trunk = pygame.Rect(
            x - trunkBredde // 2,  # Centrer stammen på x-positionen
            self.height * 0.7 - totalHeight,  # Start fra bunden og gå op
            trunkBredde,
            totalHeight

        )



        # Tegn stammen med mørkebrun farve og outline

        pygame.draw.rect(surface, (45, 30, 20), trunk)  # Indre del af stammen
        pygame.draw.rect(surface, (35, 20, 15), trunk, 2)  # Outline af stammen



        # Beregn bladenes position og størrelse
        foliageCenterY = self.height * 0.7 - totalHeight - self.height * 0.08

        foliageRadius = self.width * 0.06 * health * (1 + skadeprocent/200)
        

        # Positioner for de forskellige dele af bladene
        foliagePositions = [

            (x, foliageCenterY),  # Midten
            (x - foliageRadius * 0.7, foliageCenterY + foliageRadius * 0.3),  # Venstre

            (x + foliageRadius * 0.7, foliageCenterY + foliageRadius * 0.3),  # Højre

            (x, foliageCenterY + foliageRadius * 0.5),  # Bund

            (x, foliageCenterY - foliageRadius * 0.5),  # Top
        ]


        # Beregn farver baseret på skade
        damageFactor = 1 - health

        baseColor = (

            min(255, 200 + int(damageFactor * 55)),  # Mere rød ved skade

            max(0, 100 - int(damageFactor * 100)),   # Mindre grøn ved skade
            max(0, 150 - int(damageFactor * 150))    # Mindre blå ved skade

        )



        # Tegn alle blade
        for pos_x, pos_y in foliagePositions:

            pygame.draw.circle(surface, baseColor, (int(pos_x), int(pos_y)), int(foliageRadius))