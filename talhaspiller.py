import pygame
from config import *
import random
import math

class Spiller:
    def __init__(self, x, y, color, name):
        # Grundlæggende spiller attributter
        self.body = pygame.Rect(x, y, PLAYER_SIZE*2, PLAYER_SIZE*2)
        self.color = color
        self.name = name
        
        # Bevægelses variabler
        self.speed_x = 0  # Hastighed på x-aksen
        self.speed_y = 0  # Hastighed på y-aksen
        self.facing_right = True  # Retningsindikator
        self.on_ground = False  # Markør for jordkontakt
        self.air_dash = MAX_AIR_DASH  # Antal luftdash tilgængelige
        
        # Kamp statistikker
        self.damage = 0  # Akkumuleret skade
        self.points = 0  # Pointtæller
        self.combo = 0  # Combo tæller
        self.last_hit_time = 0  # Tidspunkt for sidste træffer
        
        # Status effekter
        self.stunned = False  # Lammelsestilstand
        self.stun_time = 0  # Varighed af lammelse
        self.is_dead = False  # Livstilstand
        self.death_timer = 0  # Nedtælling efter død
        self.recovery_frames = 0  # Genopretningsperiode
        self.invincible = False  # Udødelighed
        self.invincible_timer = 0  # Varighed af udødelighed
        
        # Dash mekanik
        self.can_dash = True  # Dash tilgængelighed
        self.dash_timer = 0  # Dash varighed/nedkøling
        self.is_dashing = False  # Dash tilstand
        self.dash_direction = 1  # Dash retning
        self.is_attacking = False  # Angrebstilstand
        
        # Combo system
        self.combo_timer = 0  # Combo varighed
        self.combo_count = 0  # Combo tæller
        self.last_attacker = None  # Seneste angriber
        
        # Partikel system
        self.particles = []  # Liste til partikler
    
    def move(self, left, right, jump, dash):
        # Tjek for død tilstand
        if self.is_dead:
            return
            
        # Håndter lammelsestilstand
        if self.stunned:
            self.stun_time -= 1
            if self.stun_time <= 0:
                self.stunned = False
            return
            
        # Hent tastatur input
        keys = pygame.key.get_pressed()
        
        # Normal bevægelse
        if not self.is_dashing:
            # Nulstil vandret hastighed hvis ingen bevægelsestaster er trykket
            if not keys[left] and not keys[right]:
                self.speed_x = 0
            elif keys[left]:
                self.speed_x = -MOVEMENT_SPEED
                self.facing_right = False
                self.dash_direction = -1
            elif keys[right]:
                self.speed_x = MOVEMENT_SPEED
                self.facing_right = True
                self.dash_direction = 1
                
            # Hop mekanik
            if keys[jump] and self.on_ground:
                self.speed_y = JUMP_FORCE
                self.on_ground = False
                self.add_jump_effect()
        
        # Opdater dash nedkøling
        if not self.can_dash:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.can_dash = True
                self.dash_timer = 0
        
        # Dash system
        if keys[dash] and self.can_dash and not self.is_dashing:
            if self.on_ground or self.air_dash > 0:
                self.start_dash()
                if not self.on_ground:
                    self.air_dash -= 1
        
        # Dash bevægelse
        if self.is_dashing:
            self.speed_x = DASH_FORCE * self.dash_direction
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.stop_dash()
        
        # Luftmodstand
        if not self.on_ground:
            self.speed_x *= AIR_RESISTANCE
    
    def start_dash(self):
        """Start a new dash"""
        self.is_dashing = True
        self.dash_timer = DASH_LENGTH
        self.can_dash = False
        self.is_attacking = True
    
    def stop_dash(self):
        """Stop the current dash"""
        self.is_dashing = False
        self.is_attacking = False
        # Starter nedkølingstiden for dash
        self.dash_timer = DASH_COOLDOWN
        self.can_dash = False
    
    def update(self, platform):
        # Hvis spilleren allerede er død, fortsæt med at være død og ikke opdater position
        if self.is_dead:
            self.speed_y += GRAVITY  # Lad dem fortsætte med at falde
            self.body.y += self.speed_y
            return True  # For at holde spilleren død
        
        # Anvend tyngdekraft
        self.speed_y += GRAVITY
        
        # Opdater position
        self.body.x += self.speed_x
        self.body.y += self.speed_y
        
        # Kun begrænse horisontal bevægelse til verdenens grænser
        if self.body.x < WORLD_LEFT_BOUNDARY:
            self.body.x = WORLD_LEFT_BOUNDARY
            self.speed_x = 0
        elif self.body.x > WORLD_RIGHT_BOUNDARY - self.body.width:
            self.body.x = WORLD_RIGHT_BOUNDARY - self.body.width
            self.speed_x = 0
        
        # Platform kollision (keep this part)
        if self.body.bottom > platform.y and self.body.top < platform.y:
            if platform.x < self.body.centerx < platform.x + platform.width:
                self.body.bottom = platform.y
                self.speed_y = 0
                self.on_ground = True
                self.air_dash = MAX_AIR_DASH
        else:
            self.on_ground = False
        
        # Opdater tæller
        if self.recovery_frames > 0:
            self.recovery_frames -= 1
        
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Opdater combo system
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0
        
        # Opdater partikler
        self.update_particles()
        
        return False
    
    def apply_knockback(self, direction, force):
        if self.invincible:
            return
            
        # Beregn tilbageslag med skade skalering
        knockback_bonus = 1 + (self.damage / 75)  # Hurtigere skalering
        total_force = min(force * knockback_bonus, MAX_KNOCKBACK)
        
        # Anvend tilbageslag med fokus på horisontal bevægelse
        self.speed_x = direction[0] * total_force * 2.0
        self.speed_y = direction[1] * total_force - 3
        
        # Stun baseret på skade
        self.stunned = True
        self.stun_time = int(8 * knockback_bonus)
        
        # Give recovery frames
        self.recovery_frames = RECOVERY_FRAMES
        
        # Tilføj hit effekt
        self.add_hit_effect()
    
    def add_hit_effect(self):
        # Tilføj partikler ved hit
        for _ in range(5):
            self.particles.append({
                'pos': [self.body.centerx, self.body.centery],
                'vel': [random.uniform(-5, 5), random.uniform(-5, 5)],
                'timer': 10,
                'color': self.color
            })
    
    def add_jump_effect(self):
        # Tilføj hop effekt
        for _ in range(3):
            self.particles.append({
                'pos': [self.body.centerx, self.body.bottom],
                'vel': [random.uniform(-2, 2), random.uniform(0, 2)],
                'timer': 5,
                'color': GRAY
            })
    
    def update_particles(self):
        # Opdater alle partikler
        for particle in self.particles[:]:
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['timer'] -= 1
            if particle['timer'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, window):
        # Tegn dash effekt når man dasher
        if self.is_dashing:
            # Tegn motion blur/dash trail
            for i in range(3):
                alpha = 100 - i * 30  # Fade out trail
                trail_offset = -self.dash_direction * i * 20
                trail_rect = self.body.copy()
                trail_rect.x += trail_offset
                
                # Opret en overflade for den semi-transparente trail
                trail_surface = pygame.Surface((trail_rect.width, trail_rect.height), pygame.SRCALPHA)
                trail_color = (*self.color[:3], alpha)
                pygame.draw.ellipse(trail_surface, trail_color, 
                                  (0, 0, trail_rect.width, trail_rect.height))
                window.blit(trail_surface, trail_rect)

        # Tegn partikler
        for particle in self.particles:
            alpha = int(255 * (particle['timer'] / 10))
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(window, color, 
                             [int(particle['pos'][0]), int(particle['pos'][1])], 3)
        
        # Tegn spiller
        pygame.draw.ellipse(window, self.color, self.body)
        
        # Tegn retningsindikator
        direction_x = self.body.centerx + (10 if self.facing_right else -10)
        pygame.draw.circle(window, BLACK, (direction_x, self.body.centery), 5)
        
        # Tegn skade tekst
        damage_text = f"{int(self.damage)}%"
        if self.combo_count > 1:
            damage_text += f" x{self.combo_count}"
        
        # Tilføj outline til tekst for bedre synlighed
        font = pygame.font.Font(None, MEDIUM_FONT)
        text = font.render(damage_text, True, BLACK)
        text_outline = font.render(damage_text, True, WHITE)
        text_rect = text.get_rect(center=(self.body.centerx, self.body.top - 30))
        
        # Tegn outline først og tekst derefter
        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            window.blit(text_outline, (text_rect.x + dx, text_rect.y + dy))
        window.blit(text, text_rect)
        
        # Tegn dash nedkøling indikator
        cooldown_radius = 15
        cooldown_y = self.body.top - 60  # Position over skade tekst
        
        # Tegn baggrundscirkel
        pygame.draw.circle(window, (50, 50, 50), (self.body.centerx, cooldown_y), cooldown_radius)
        
        if not self.can_dash:
            # Beregn cooldown progress (0 til 1)
            progress = self.dash_timer / DASH_COOLDOWN
            
            # Tegn arc til at vise cooldown (fuld ud som cooldown fortsætter)
            angle = progress * 360  # Konverter progress til grader
            
            # Tegn udfyldt arc
            surface = pygame.Surface((cooldown_radius * 2, cooldown_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color[:3], 128), 
                             (cooldown_radius, cooldown_radius), cooldown_radius)
            
            # Opret masken for arc
            mask = pygame.Surface((cooldown_radius * 2, cooldown_radius * 2), pygame.SRCALPHA)
            pygame.draw.arc(mask, (255, 255, 255, 255),
                          (0, 0, cooldown_radius * 2, cooldown_radius * 2),
                          0, math.radians(angle), cooldown_radius)
            
            # Anvend masken til surfacen
            surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            window.blit(surface, 
                       (self.body.centerx - cooldown_radius, 
                        cooldown_y - cooldown_radius))
        else:
            # Tegn r indikator
            pygame.draw.circle(window, self.color, 
                             (self.body.centerx, cooldown_y), cooldown_radius - 2)
    
    def get_center(self):
        return (self.body.centerx, self.body.centery)
    
    def has_fallen(self):
        """Tjek om spilleren er faldet i void"""
        # Betragt faldet hvis spilleren er langt under platformen
        return self.body.top > HEIGHT - (HEIGHT * 0.2)  # Øget void område
    
    def start_position(self):
        """Sæt spillerens position til start"""
        self.is_dead = False
        self.death_timer = 0
        self.damage = 0
        self.combo_count = 0
        self.combo_timer = 0
        self.last_attacker = None
        self.speed_x = 0
        self.speed_y = 0
        self.stunned = False
        self.stun_time = 0
        self.is_dashing = False
        self.can_dash = True
        self.dash_timer = 0
        self.air_dash = MAX_AIR_DASH
        self.particles = [] 