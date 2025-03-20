import pygame
import math
import time
import sys
import os
from config import *
from talhaspiller import Spiller
from bane2 import Bane
from main import Menu  # Add this import

class GameState:
    MENU = 0
    BATTLE = 1
    PAUSE = 2
    ROUND_END = 3
    GAME_OVER = 4

def display_points(window, spiller1, spiller2, time_left):
    # Top bar background
    pygame.draw.rect(window, GRAY, (0, 0, WIDTH, 50))
    
    # Players' points and names
    p1_text = f"{spiller1.name}: {spiller1.points}"
    p2_text = f"{spiller2.name}: {spiller2.points}"
    
    font = pygame.font.Font(None, MEDIUM_FONT)
    p1_render = font.render(p1_text, True, RED)
    p2_render = font.render(p2_text, True, BLUE)
    
    window.blit(p1_render, (20, 10))
    window.blit(p2_render, (WIDTH - 20 - p2_render.get_width(), 10))
    
    # Timer in the middle
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    time_text = f"{minutes}:{seconds:02d}"
    time_render = font.render(time_text, True, BLACK)
    window.blit(time_render, (WIDTH//2 - time_render.get_width()//2, 10))

def display_round_start(window, round_num):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    window.blit(overlay, (0, 0))
    
    # Draw round number with larger font
    font = pygame.font.Font(None, LARGE_FONT)
    text = font.render(f"Runde {round_num}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    window.blit(text, text_rect)

def display_winner(window, winner):
    # Background overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    window.blit(overlay, (0, 0))
    
    # Winner text
    font = pygame.font.Font(None, LARGE_FONT)
    text = font.render(f"{winner.name} Wins!", True, GOLD)
    window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
    
    # Instructions
    font = pygame.font.Font(None, SMALL_FONT)
    text = font.render("Press SPACE to start a new match", True, WHITE)
    window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 50))

def handle_collision(spiller1, spiller2):
    """Handle collision between two players"""
    # Find distance between players
    center1 = spiller1.get_center()
    center2 = spiller2.get_center()
    distance = math.dist(center1, center2)
    
    # If players are touching
    if distance < PLAYER_SIZE * 2 and not (spiller1.is_dead or spiller2.is_dead):
        # Determine direction based on players' position and direction
        direction = 1 if center1[0] < center2[0] else -1
        
        # Calculate force based on speed and dash
        spiller1_force = abs(spiller1.speed_x) * (1.5 if spiller1.is_dashing else 1)
        spiller2_force = abs(spiller2.speed_x) * (1.5 if spiller2.is_dashing else 1)
        
        # Apply damage and knockback based on who is most active
        if (spiller1.is_dashing or spiller1_force > 2) and spiller2.recovery_frames == 0:
            force = BASE_KNOCKBACK * (1.8 if spiller1.is_dashing else 1)
            force *= (1 + spiller2.damage / 100)
            
            # Update combo system
            if spiller1 == spiller2.last_attacker:
                spiller2.combo_count += 1
            else:
                spiller2.combo_count = 1
            spiller2.last_attacker = spiller1
            spiller2.combo_timer = 120
            
            # Less damage on dash
            damage = DAMAGE_AMOUNT * (DASH_DAMAGE_BONUS if spiller1.is_dashing else 1)
            spiller2.damage = min(spiller2.damage + damage, MAX_DAMAGE)
            spiller2.apply_knockback((direction, -0.15), force)
            
        if (spiller2.is_dashing or spiller2_force > 2) and spiller1.recovery_frames == 0:
            force = BASE_KNOCKBACK * (1.8 if spiller2.is_dashing else 1)
            force *= (1 + spiller1.damage / 100)
            
            # Update combo system
            if spiller2 == spiller1.last_attacker:
                spiller1.combo_count += 1
            else:
                spiller1.combo_count = 1
            spiller1.last_attacker = spiller2
            spiller1.combo_timer = 120
            
            # Less damage on dash
            damage = DAMAGE_AMOUNT * (DASH_DAMAGE_BONUS if spiller2.is_dashing else 1)
            spiller1.damage = min(spiller1.damage + damage, MAX_DAMAGE)
            spiller1.apply_knockback((-direction, -0.15), force)
        
        # Push players apart to avoid overlap
        overlap = PLAYER_SIZE * 2 - distance
        if center1[0] < center2[0]:
            spiller1.body.x -= overlap / 2
            spiller2.body.x += overlap / 2
        else:
            spiller1.body.x += overlap / 2
            spiller2.body.x -= overlap / 2

def display_round_winner(window, winner_name, winner_color):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    window.blit(overlay, (0, 0))
    
    font = pygame.font.Font(None, LARGE_FONT)
    text = font.render(f"{winner_name} har vundet runden!", True, winner_color)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    window.blit(text, text_rect)
    
    font = pygame.font.Font(None, MEDIUM_FONT)
    text = font.render("Tryk MELLEMRUM for næste runde", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    window.blit(text, text_rect)

def display_game_winner(window, winner_name, winner_color):
    # Create semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    window.blit(overlay, (0, 0))
    
    # Display winner text
    font = pygame.font.Font(None, LARGE_FONT)
    winner_text = font.render(f"{winner_name} vandt spillet!", True, winner_color)
    text_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    window.blit(winner_text, text_rect)
    
    # Display options
    font = pygame.font.Font(None, MEDIUM_FONT)
    new_game_text = font.render("Tryk MELLEMRUM for nyt spil", True, WHITE)
    menu_text = font.render("Tryk ESC for hovedmenu", True, WHITE)
    
    new_game_rect = new_game_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
    
    window.blit(new_game_text, new_game_rect)
    window.blit(menu_text, menu_rect)

def main():
    """Main game loop"""
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()  # Initialize mixer for menu sounds
    
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sumo Battle!")
    
    # Create menu
    menu = Menu(WIDTH, HEIGHT)
    
    # Create the Japanese themed map first
    bane = Bane(WIDTH, HEIGHT)
    
    # Create players with fixed spawn positions - using platform from bane
    platform = bane.platform_segments[0]  # Get the platform from bane
    spiller1 = Spiller(platform.x + SPAWN_DISTANCE, 
                      platform.y - SPAWN_HEIGHT, RED, "Rød Spiller")
    spiller2 = Spiller(platform.x + platform.width - SPAWN_DISTANCE, 
                      platform.y - SPAWN_HEIGHT, BLUE, "Blå Spiller")
    
    clock = pygame.time.Clock()
    running = True
    
    # Game state - start with MENU instead of BATTLE
    state = GameState.MENU
    round_num = 1
    round_start_time = time.time()
    
    # Add these variables for respawn timing
    RESPAWN_DELAY = 1500  # 1.5 seconds in milliseconds
    respawn_timer = 0
    waiting_for_respawn = False
    
    # Add these variables for round start display
    ROUND_START_DELAY = 2000  # 2 seconds to show round number
    round_start_display_timer = 0
    showing_round_start = False
    
    def reset_round():
        nonlocal showing_round_start, round_start_display_timer, round_winner
        # Reset player positions
        spiller1.body.x = platform.x + SPAWN_DISTANCE
        spiller1.body.y = platform.y - SPAWN_HEIGHT
        spiller2.body.x = platform.x + platform.width - SPAWN_DISTANCE
        spiller2.body.y = platform.y - SPAWN_HEIGHT
        spiller1.start_position()
        spiller2.start_position()
        # Reset dead state
        spiller1.is_dead = False
        spiller2.is_dead = False
        # Reset round winner
        round_winner = None
        # Show round start display
        showing_round_start = True
        round_start_display_timer = pygame.time.get_ticks()
    
    # Track who fell first
    first_to_fall = None
    # Track the winner of the current round
    round_winner = None
    
    while running:
        if state == GameState.MENU:
            window.fill((0, 0, 0))
            menu.draw(window)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                action = menu.handle_input(event)
                if action == "Start Game":
                    state = GameState.BATTLE
                    pygame.mixer.music.stop()  # Stop menu music
                elif action == "Quit":
                    running = False
                    
        elif state == GameState.BATTLE:
            # Handle regular game events first
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = GameState.MENU
                        pygame.mixer.music.play(-1)  # Resume menu music
                    elif event.key == pygame.K_p:
                        state = GameState.PAUSE
            
            now = time.time()
            time_left = max(0, ROUND_TIME - (now - round_start_time))
            current_time = pygame.time.get_ticks()
            
            # Tegn banen med spillernes skadeprocent
            bane.draw(window, spiller1, spiller2)
            
            # Only update players if not showing round start
            if not showing_round_start:
                # Update players
                if not spiller1.is_dead:
                    spiller1.move(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
                if not spiller2.is_dead:
                    spiller2.move(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
                
                # Check for void falls
                if not waiting_for_respawn:  # Only check for falls if round is not over
                    if not spiller1.is_dead and spiller1.body.top > platform.y:  # If player is below platform
                        spiller1.is_dead = True
                        if first_to_fall is None:
                            first_to_fall = 1
                    
                    if not spiller2.is_dead and spiller2.body.top > platform.y:  # If player is below platform
                        spiller2.is_dead = True
                        if first_to_fall is None:
                            first_to_fall = 2
                
                # Update players
                if not spiller1.is_dead:
                    spiller1.update(platform)
                if not spiller2.is_dead:
                    spiller2.update(platform)
                
                # Handle collisions if both players are alive
                if not spiller1.is_dead and not spiller2.is_dead:
                    handle_collision(spiller1, spiller2)
                
                # Check for round end
                if not waiting_for_respawn and (spiller1.is_dead or spiller2.is_dead):
                    waiting_for_respawn = True
                    respawn_timer = current_time
                    
                    # Award point based on who fell first
                    if first_to_fall == 1:  # Red fell first, Blue wins
                        spiller2.points += 1
                        round_winner = "blue"
                        display_round_winner(window, "Blå Spiller", BLUE)
                    elif first_to_fall == 2:  # Blue fell first, Red wins
                        spiller1.points += 1
                        round_winner = "red"
                        display_round_winner(window, "Rød Spiller", RED)
                    else:  # If no one has fallen yet, but someone is dead
                        if spiller1.is_dead:  # Red is dead, Blue wins
                            spiller2.points += 1
                            round_winner = "blue"
                            display_round_winner(window, "Blå Spiller", BLUE)
                        else:  # Blue is dead, Red wins
                            spiller1.points += 1
                            round_winner = "red"
                            display_round_winner(window, "Rød Spiller", RED)
                    
                    # Reset first_to_fall for next round but keep track of who won
                    first_to_fall = None
                    
                    # Check if game is over
                    if spiller1.points >= MAX_POINTS or spiller2.points >= MAX_POINTS:
                        state = GameState.GAME_OVER
                        winner_name = "Rød Spiller" if spiller1.points > spiller2.points else "Blå Spiller"
                        winner_color = RED if spiller1.points > spiller2.points else BLUE
                        display_game_winner(window, winner_name, winner_color)
            
            # Handle respawn timing
            if waiting_for_respawn and current_time - respawn_timer >= RESPAWN_DELAY:
                waiting_for_respawn = False
                round_num += 1
                round_start_time = time.time()
                reset_round()
            
            # Draw players
            spiller1.draw(window)
            spiller2.draw(window)
            
            # Draw UI on top
            display_points(window, spiller1, spiller2, time_left)
            
            # Show round start display
            if showing_round_start:
                display_round_start(window, round_num)
                if current_time - round_start_display_timer >= ROUND_START_DELAY:
                    showing_round_start = False
            
            # If waiting for respawn, keep showing the winner message
            elif waiting_for_respawn:
                if round_winner == "blue":
                    display_round_winner(window, "Blå Spiller", BLUE)
                elif round_winner == "red":
                    display_round_winner(window, "Rød Spiller", RED)
        
        elif state == GameState.GAME_OVER:
            # Draw the map as background
            bane.draw(window)
            spiller1.draw(window)
            spiller2.draw(window)
            display_points(window, spiller1, spiller2, time_left)
            winner_name = "Rød Spiller" if spiller1.points > spiller2.points else "Blå Spiller"
            winner_color = RED if spiller1.points > spiller2.points else BLUE
            display_game_winner(window, winner_name, winner_color)
            
            # Check for new game or return to menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Clean up resources
                        pygame.mixer.music.stop()
                        pygame.quit()
                        # Restart the game
                        python = sys.executable
                        os.execl(python, python, *sys.argv)
                    elif event.key == pygame.K_ESCAPE:
                        # Return to main menu
                        state = GameState.MENU
                        spiller1.points = 0
                        spiller2.points = 0
                        reset_round()
                        round_num = 1
                        round_start_time = time.time()
                        pygame.mixer.music.play(-1)  # Resume menu music
        
        elif state == GameState.PAUSE:
            # Draw the map as background for pause screen
            bane.draw(window)
            spiller1.draw(window)
            spiller2.draw(window)
            display_points(window, spiller1, spiller2, time_left)
            
            # Show pause screen
            font = pygame.font.Font(None, LARGE_FONT)
            text = font.render("PAUSE", True, BLACK)
            window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
            
            font = pygame.font.Font(None, SMALL_FONT)
            text = font.render("Tryk ESC for at fortsætte", True, BLACK)
            window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 50))
        
        pygame.display.update()
        clock.tick(FRAME_RATE)
    
    pygame.quit()

if __name__ == "__main__":
    main() 