import pygame
from bane2 import Bane
import os
import math
import random

class Menu:
    def __init__(self, width, height):
        # gem skærmens dimensioner som attributter
        self.width = width
        
        self.height = height
        
        # gammelt forsøg på at indlæse den her skrifttype, men vi bruger bare standard font nu
        try:
            self.title_font = pygame.font.Font("assets/fonts/yumin.ttf", 100)
        except:
            self.title_font = pygame.font.Font(None, 100)
        self.menu_font = pygame.font.Font(None, 50)
        
        # menu valgmuligheder og knapper
        self.options = ["Start Game", "Quit"]
        self.selected = 0  # indeks for valgt menupunkt
        self.buttons = []  # liste til rektangler for hver menu mulighed
        
        # farve definitioner
        self.title_color = (200, 0, 0)  # rød titel farve
        self.selected_color = (255, 215, 0)  # guld farve til valgt punkt
        self.unselected_color = (255, 255, 255)  # hvid farve til ikke valgte punkter
        
        # baggrunds animation
        self.circles = []
        for _ in range(20):
            self.circles.append({
                'x': random.randint(0, width),  # tilfældig x position
                'y': random.randint(0, height),  # tilfældig y position
                'size': random.randint(50, 150),  # tilfældig størrelse
                'speed': random.uniform(0.5, 2)  # tilfældig hastighed
            })
        
        # initialiser lydmixer hvis ikke allerede initialiseret
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # indlæs og afspil baggrundsmusik
        try:
            pygame.mixer.music.load("assets/mainmenu.mp3")
            pygame.mixer.music.set_volume(0.5)  # lydstyrke sat til 50%
            pygame.mixer.music.play(-1)  # -1 betyder uendelig gentagelse
        except Exception as e:
            print(f"Advarsel: Kunne ikke indlæse mainmenu.mp3: {e}")
            
        # lydeffekter
        self.hover_sound = None  # lyd ved markør over menupunkt
        self.select_sound = None  # lyd ved valg af menupunkt
        try:
            self.hover_sound = pygame.mixer.Sound("assets/hover.wav") # DER ER IKKE NOGEN HOVER SOUND; ELLER SELECT, GAMMEL KODE!!!
            self.select_sound = pygame.mixer.Sound("assets/select.wav")
        except:
            print("Advarsel: Kunne ikke indlæse lydeffekter")

    def draw_background(self, screen):
        """tegn animeret baggrund med cirkler"""
        # update og tegn hver cirkel
        for circle in self.circles:
            # update y position med hastighed
            circle['y'] = (circle['y'] + circle['speed']) % self.height
            
            # tegn cirkel med gennemsigtighed
            surface = pygame.Surface((circle['size'], circle['size']), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 255, 255, 30), 
                             (circle['size']//2, circle['size']//2), 
                             circle['size']//2)
            screen.blit(surface, (circle['x'], circle['y']))
    
    def draw(self, screen):
        """tegn hele menuen"""
        # tegn sort baggrund
        screen.fill((0, 0, 0))
        
        # tegn animeret baggrund
        self.draw_background(screen)
        
        # tegn titel
        title = self.title_font.render("Sumo Slammers", True, self.title_color)
        title_rect = title.get_rect(center=(self.width//2, self.height//4))
        screen.blit(title, title_rect)
        
        # tegn menu muligheder
        button_height = 50
        start_y = self.height//2
        self.buttons = []  # nulstil knapliste
        
        # tegn hver menu mulighed
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected else self.unselected_color
            text = self.menu_font.render(option, True, color)
            rect = text.get_rect(center=(self.width//2, start_y + i * button_height))
            screen.blit(text, rect)
            self.buttons.append(rect)
    
    def handle_input(self, event):
        """håndter bruger input"""
        if event.type == pygame.KEYDOWN:
            # naviger op/ned i menuen
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
                if self.hover_sound:
                    self.hover_sound.play()
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
                if self.hover_sound:
                    self.hover_sound.play()
            # vælg menu punkt ved enter/space
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.select_sound:
                    self.select_sound.play()
                return self.options[self.selected]
        
        # håndter mus input
        elif event.type == pygame.MOUSEMOTION:
            # tjek for markør over menupunkter
            for i, rect in enumerate(self.buttons):
                if rect.collidepoint(event.pos):
                    if self.selected != i:
                        self.selected = i
                        if self.hover_sound:
                            self.hover_sound.play()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # tjek for klik på menupunkter
            if event.button == 1:  # venstre museklik
                for i, rect in enumerate(self.buttons):
                    if rect.collidepoint(event.pos):
                        if self.select_sound:
                            self.select_sound.play()
                        return self.options[i]
        
        return None  # ingen handling valgt