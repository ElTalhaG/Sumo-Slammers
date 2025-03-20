import pygame
from bane2 import Bane
import os
import math
import random

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Font setup - try to load a Japanese-style font, fallback to default if not found
        try:
            self.title_font = pygame.font.Font("assets/fonts/yumin.ttf", 100)
        except:
            self.title_font = pygame.font.Font(None, 100)
        self.menu_font = pygame.font.Font(None, 50)
        
        # Menu options and buttons
        self.options = ["Start Game", "Controls", "Quit"]
        self.selected = 0
        self.buttons = []  # Will store rect for each menu option
        
        # Colors
        self.title_color = (200, 0, 0)
        self.selected_color = (255, 215, 0)
        self.unselected_color = (255, 255, 255)
        
        # Background animation
        self.circles = []
        for _ in range(20):
            self.circles.append({
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'size': random.randint(50, 150),
                'speed': random.uniform(0.5, 2)
            })
        
        # Initialize mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # Load and play background music
        try:
            pygame.mixer.music.load("assets/mainmenu.mp3")
            pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except Exception as e:
            print(f"Warning: Could not load mainmenu.mp3: {e}")
            
        # Sound effects
        self.hover_sound = None
        self.select_sound = None
        try:
            self.hover_sound = pygame.mixer.Sound("assets/hover.wav")
            self.select_sound = pygame.mixer.Sound("assets/select.wav")
        except:
            print("Warning: Could not load sound effects")

    def draw_background(self, screen):
        # Fill with dark gradient
        for y in range(self.height):
            color_value = max(20, min(50, 20 + y * 30 // self.height))
            pygame.draw.line(screen, (color_value, 0, color_value), 
                           (0, y), (self.width, y))
        
        # Animate and draw circles
        for circle in self.circles:
            circle['y'] = (circle['y'] + circle['speed']) % self.height
            alpha_surface = pygame.Surface((circle['size'], circle['size']), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surface, (255, 0, 0, 30), 
                             (circle['size']//2, circle['size']//2), circle['size']//2)
            screen.blit(alpha_surface, (circle['x'] - circle['size']//2, circle['y'] - circle['size']//2))

    def draw(self, screen):
        # Draw animated background
        self.draw_background(screen)
        
        # Draw title with Japanese-style effect
        title = self.title_font.render("SUMO SLAMMERS", True, self.title_color)
        title_shadow = self.title_font.render("SUMO SLAMMERS", True, (0, 0, 0))
        
        # Add wave effect to title
        time = pygame.time.get_ticks() / 1000
        title_y_offset = math.sin(time * 2) * 10
        
        title_rect = title.get_rect(center=(self.width//2 + 4, self.height//4 + 4 + title_y_offset))
        screen.blit(title_shadow, title_rect)
        title_rect = title.get_rect(center=(self.width//2, self.height//4 + title_y_offset))
        screen.blit(title, title_rect)
        
        # Draw menu options and store their rects
        self.buttons = []  # Clear previous buttons
        for i, option in enumerate(self.options):
            # Create button background
            button_rect = pygame.Rect(
                self.width//2 - 100,
                self.height//2 + i * 60 - 10,
                200, 50
            )
            self.buttons.append(button_rect)
            
            # Check if mouse is hovering
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = button_rect.collidepoint(mouse_pos)
            is_selected = i == self.selected
            
            # Draw button background
            if is_hovered or is_selected:
                pygame.draw.rect(screen, (100, 0, 0), button_rect)
                color = self.selected_color
            else:
                pygame.draw.rect(screen, (50, 0, 0), button_rect)
                color = self.unselected_color
            
            # Draw button text
            text = self.menu_font.render(option, True, color)
            rect = text.get_rect(center=(self.width//2, self.height//2 + i * 60))
            screen.blit(text, rect)

    def handle_input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle mouse movement
        if event.type == pygame.MOUSEMOTION:
            for i, button in enumerate(self.buttons):
                if button.collidepoint(mouse_pos) and self.selected != i:
                    self.selected = i
                    if self.hover_sound:
                        self.hover_sound.play()
        
        # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                for i, button in enumerate(self.buttons):
                    if button.collidepoint(mouse_pos):
                        if self.select_sound:
                            self.select_sound.play()
                        return self.options[i]
        
        # Handle keyboard
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
                if self.hover_sound:
                    self.hover_sound.play()
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
                if self.hover_sound:
                    self.hover_sound.play()
            elif event.key == pygame.K_RETURN:
                if self.select_sound:
                    self.select_sound.play()
                return self.options[self.selected]
        return None

