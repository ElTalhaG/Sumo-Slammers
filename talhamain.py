# Af Talha og Azad (fælles kode stumper)
import pygame
import math
import time
import sys
import os
from config import *
from talhaspiller import Spiller
from bane2 import Bane
from main import Menu  # Tilføj denne import

class GameState:
    """
    Enumeration af spillets tilstande.
    """
    MENU = 0      # Hovedmenu tilstand
    BATTLE = 1    # Kamp tilstand
    PAUSE = 2     # Pause tilstand
    ROUND_END = 3 # Runde afslutning
    GAME_OVER = 4 # Spil afslutning

def display_points(window, spiller1, spiller2, time_left):
    """
    Viser spillernes point og den resterende tid i toppen af skærmen.
    
    Parametre:
        window: Pygame vindue at tegne på
        spiller1: Første spiller objekt
        spiller2: Anden spiller objekt
        time_left: Resterende tid i sekunder
    """
    pygame.draw.rect(window, GRAY, (0, 0, WIDTH, 50))  # Tegner en grå rektangel som baggrund for pointvisning
    p1_text = f"{spiller1.name}: {spiller1.points}"  # Formaterer tekst til spiller 1's navn og point
    p2_text = f"{spiller2.name}: {spiller2.points}"  # Formaterer tekst til spiller 2's navn og point
    font = pygame.font.Font(None, MEDIUM_FONT)  # Opretter en skrifttype til teksten
    p1_render = font.render(p1_text, True, RED)  # Render tekst for spiller 1 i rød farve
    p2_render = font.render(p2_text, True, BLUE)  # Render tekst for spiller 2 i blå farve
    window.blit(p1_render, (20, 10))  # Tegner spiller 1's tekst på skærmen
    window.blit(p2_render, (WIDTH - 20 - p2_render.get_width(), 10))  # Tegner spiller 2's tekst på skærmen
    minutes = int(time_left // 60)  # Beregner antal minutter tilbage
    seconds = int(time_left % 60)  # Beregner antal sekunder tilbage
    time_text = f"{minutes}:{seconds:02d}"  # Formaterer tidstekst
    time_render = font.render(time_text, True, BLACK)  # Render tidstekst i sort farve
    window.blit(time_render, (WIDTH//2 - time_render.get_width()//2, 10))  # Tegner tidstekst i midten af skærmen

def display_round_start(window, round_num):
    """
    Viser rundenummeret ved start af en ny runde.
    
    Parametre:
        window: Pygame vindue at tegne på
        round_num: Aktuelle rundenummer
    """
    overlay = pygame.Surface((WIDTH, HEIGHT))  # Opretter et overlag til at dække hele skærmen
    overlay.set_alpha(128)  # Sætter gennemsigtighed for overlaget
    overlay.fill(BLACK)  # Fylder overlaget med sort farve
    window.blit(overlay, (0, 0))  # Tegner overlaget på skærmen
    font = pygame.font.Font(None, LARGE_FONT)  # Opretter en stor skrifttype til rundenummer
    text = font.render(f"Runde {round_num}", True, WHITE)  # Render rundenummer tekst i hvid farve
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))  # Centrering af tekst på skærmen
    window.blit(text, text_rect)  # Tegner rundenummer tekst på skærmen

def display_winner(window, winner):
    """
    Viser vinderen af spillet og instruktioner til at starte et nyt spil.
    
    Parametre:
        window: Pygame vindue at tegne på
        winner: Vinder-objektet med navn og farve
    """
    overlay = pygame.Surface((WIDTH, HEIGHT))  # Opretter et overlag til at dække hele skærmen
    overlay.set_alpha(128)  # Sætter gennemsigtighed for overlaget
    overlay.fill(BLACK)  # Fylder overlaget med sort farve
    window.blit(overlay, (0, 0))  # Tegner overlaget på skærmen
    font = pygame.font.Font(None, LARGE_FONT)  # Opretter en stor skrifttype til vinder tekst
    text = font.render(f"{winner.name} Wins!", True, GOLD)  # Render vinder tekst i guld farve
    window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))  # Tegner vinder tekst på skærmen
    font = pygame.font.Font(None, SMALL_FONT)  # Opretter en lille skrifttype til instruktioner
    text = font.render("Tryk MELLEMRUM for at starte en ny kamp", True, WHITE)  # Render instruktioner i hvid farve
    window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 50))  # Tegner instruktioner på skærmen

def handle_collision(spiller1, spiller2, punch_sound=None):
    """
    Håndterer kollision mellem to spillere.
    
    Parametre:
        spiller1: Første spiller objekt
        spiller2: Anden spiller objekt
        punch_sound: Lydefekt for kollision (valgfri)
    """
    center1 = spiller1.get_center()  # Henter centrum af spiller 1
    center2 = spiller2.get_center()  # Henter centrum af spiller 2
    distance = math.dist(center1, center2)  # Beregner afstand mellem spillere
    if distance < PLAYER_SIZE * 2 and not (spiller1.is_dead or spiller2.is_dead):  # Tjekker om spillere rører hinanden
        if punch_sound:  # Hvis der er en lydeffekt tilgængelig
            punch_sound.play()  # Afspil lydeffekt
        direction = 1 if center1[0] < center2[0] else -1  # Bestemmer retning baseret på position
        spiller1_force = abs(spiller1.speed_x) * (1.5 if spiller1.is_dashing else 1)  # Beregner kraft for spiller 1
        spiller2_force = abs(spiller2.speed_x) * (1.5 if spiller2.is_dashing else 1)  # Beregner kraft for spiller 2
        if (spiller1.is_dashing or spiller1_force > 2) and spiller2.recovery_frames == 0:  # Tjekker om spiller 1 angriber
            force = BASE_KNOCKBACK * (1.8 if spiller1.is_dashing else 1)  # Beregner knockback kraft
            force *= (1 + spiller2.damage / 100)  # Øg kraft baseret på skadeprocent (jo mere skade, jo længere knockback)
            if spiller1 == spiller2.last_attacker:  # Opdaterer combo system
                spiller2.combo_count += 1
            else:
                spiller2.combo_count = 1
            spiller2.last_attacker = spiller1
            spiller2.combo_timer = 120
            damage = DAMAGE_AMOUNT * (DASH_DAMAGE_BONUS if spiller1.is_dashing else 1)  # Beregner skade
            spiller2.damage = min(spiller2.damage + damage, MAX_DAMAGE)  # Opdaterer skade
            spiller2.apply_knockback((direction, -0.15), force)  # Anvender knockback
        if (spiller2.is_dashing or spiller2_force > 2) and spiller1.recovery_frames == 0:  # Tjekker om spiller 2 angriber
            force = BASE_KNOCKBACK * (1.8 if spiller2.is_dashing else 1)  # Beregner knockback kraft
            force *= (1 + spiller1.damage / 100)  # Justerer kraft baseret på skade
            if spiller2 == spiller1.last_attacker:  # Opdaterer combo system
                spiller1.combo_count += 1
            else:
                spiller1.combo_count = 1
            spiller1.last_attacker = spiller2
            spiller1.combo_timer = 120
            damage = DAMAGE_AMOUNT * (DASH_DAMAGE_BONUS if spiller2.is_dashing else 1)  # Beregner skade
            spiller1.damage = min(spiller1.damage + damage, MAX_DAMAGE)  # Opdaterer skade
            spiller1.apply_knockback((-direction, -0.15), force)  # Anvender knockback
        overlap = PLAYER_SIZE * 2 - distance  # Beregner overlap for at undgå overlap
        if center1[0] < center2[0]:  # Justerer positioner for at undgå overlap
            spiller1.body.x -= overlap / 2
            spiller2.body.x += overlap / 2
        else:
            spiller1.body.x += overlap / 2
            spiller2.body.x -= overlap / 2

def display_round_winner(window, winner_name, winner_color):
    """
    Viser vinderen af runden og instruktioner til næste runde.
    
    Parametre:
        window: Pygame vindue at tegne på
        winner_name: Vinderens navn
        winner_color: Vinderens farve
    """
    overlay = pygame.Surface((WIDTH, HEIGHT))  # Opretter et overlag til at dække hele skærmen
    overlay.set_alpha(128)  # Sætter gennemsigtighed for overlaget
    overlay.fill(BLACK)  # Fylder overlaget med sort farve
    window.blit(overlay, (0, 0))  # Tegner overlaget på skærmen
    font = pygame.font.Font(None, LARGE_FONT)  # Opretter en stor skrifttype til vinder tekst
    text = font.render(f"{winner_name} har vundet runden!", True, winner_color)  # Render vinder tekst i vinderens farve
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))  # Centrering af tekst på skærmen
    window.blit(text, text_rect)  # Tegner vinder tekst på skærmen
    font = pygame.font.Font(None, MEDIUM_FONT)  # Opretter en medium skrifttype til instruktioner
    text = font.render("Tryk MELLEMRUM for næste runde", True, WHITE)  # Render instruktioner i hvid farve
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))  # Centrering af instruktioner
    window.blit(text, text_rect)  # Tegner instruktioner på skærmen

def display_game_winner(window, winner_name, winner_color):
    """
    Viser vinderen af hele spillet og muligheder for at fortsætte.
    
    Parametre:
        window: Pygame vindue at tegne på
        winner_name: Vinderens navn
        winner_color: Vinderens farve
    """
    overlay = pygame.Surface((WIDTH, HEIGHT))  # Opretter et overlag til at dække hele skærmen
    overlay.set_alpha(128)  # Sætter gennemsigtighed for overlaget
    overlay.fill(BLACK)  # Fylder overlaget med sort farve
    window.blit(overlay, (0, 0))  # Tegner overlaget på skærmen
    font = pygame.font.Font(None, LARGE_FONT)  # Opretter en stor skrifttype til vinder tekst
    winner_text = font.render(f"{winner_name} vandt spillet!", True, winner_color)  # Render vinder tekst i vinderens farve
    text_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))  # Centrering af vinder tekst
    window.blit(winner_text, text_rect)  # Tegner vinder tekst på skærmen
    font = pygame.font.Font(None, MEDIUM_FONT)  # Opretter en medium skrifttype til valgmuligheder
    new_game_text = font.render("Tryk MELLEMRUM for nyt spil", True, WHITE)  # Render tekst for nyt spil i hvid farve
    menu_text = font.render("Tryk ESC for hovedmenu", True, WHITE)  # Render tekst for hovedmenu i hvid farve
    new_game_rect = new_game_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))  # Centrering af nyt spil tekst
    menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))  # Centrering af hovedmenu tekst
    window.blit(new_game_text, new_game_rect)  # Tegner nyt spil tekst på skærmen
    window.blit(menu_text, menu_rect)  # Tegner hovedmenu tekst på skærmen

def main():
    """
    Hovedspilsløkke og initialisering af spillet.
    """
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()  # Initialiser mixer til menu lyde
    
    # Indlæs lydeffekter
    try:
        punch_sound = pygame.mixer.Sound("assets/punch.mp3")
        punch_sound.set_volume(0.4)  # Sæt lydstyrke til 40%
    except:
        print("Advarsel: Kunne ikke indlæse punch.mp3")
        punch_sound = None
    
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sumo Battle!")
    
    # Opret menu
    menu = Menu(WIDTH, HEIGHT)
    
    # Opret den japansk-inspirerede bane først
    bane = Bane(WIDTH, HEIGHT)
    
    # Opret spillere med faste startpositioner - brug platform fra banen
    platform = bane.platformSegments[0]  # Hent platformen fra banen
    spiller1 = Spiller(platform.x + SPAWN_DISTANCE, 
                      platform.y - SPAWN_HEIGHT, RED, "Rød Spiller")
    spiller2 = Spiller(platform.x + platform.width - SPAWN_DISTANCE, 
                      platform.y - SPAWN_HEIGHT, BLUE, "Blå Spiller")
    
    clock = pygame.time.Clock()
    running = True
    
    # Spiltilstand - start med MENU i stedet for BATTLE
    state = GameState.MENU
    round_num = 1
    round_start_time = time.time()
    
    # Tilføj disse variabler for respawn timing
    RESPAWN_DELAY = 1500  # 1.5 sekunder i millisekunder
    respawn_timer = 0
    waiting_for_respawn = False
    
    # Tilføj disse variabler for visning af rundestart
    ROUND_START_DELAY = 2000  # 2 sekunder til at vise rundenummer
    round_start_display_timer = 0
    showing_round_start = False
    
    def reset_round():
        """
        Nulstiller runden ved at genstarte spillernes positioner og tilstand.
        """
        nonlocal showing_round_start, round_start_display_timer, round_winner
        spiller1.body.x = platform.x + SPAWN_DISTANCE  # Nulstiller spiller 1's x-position
        spiller1.body.y = platform.y - SPAWN_HEIGHT  # Nulstiller spiller 1's y-position
        spiller2.body.x = platform.x + platform.width - SPAWN_DISTANCE  # Nulstiller spiller 2's x-position
        spiller2.body.y = platform.y - SPAWN_HEIGHT  # Nulstiller spiller 2's y-position
        spiller1.start_position()  # Nulstiller spiller 1's startposition
        spiller2.start_position()  # Nulstiller spiller 2's startposition
        spiller1.is_dead = False  # Nulstiller spiller 1's død tilstand
        spiller2.is_dead = False  # Nulstiller spiller 2's død tilstand
        round_winner = None  # Nulstiller rundevinder
        showing_round_start = True  # Sætter til at vise rundestart
        round_start_display_timer = pygame.time.get_ticks()  # Gemmer nuværende tid for rundestart display
    
    # Hold styr på hvem der faldt først
    first_to_fall = None
    # Hold styr på vinderen af den aktuelle runde
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
                    pygame.mixer.music.stop()  # Stop menu musik
                elif action == "Quit":
                    running = False
                    
        elif state == GameState.BATTLE:
            # Håndter almindelige spilhændelser først
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = GameState.MENU
                        pygame.mixer.music.play(-1)  # Genoptag menu musik
                    elif event.key == pygame.K_p:
                        state = GameState.PAUSE
            
            now = time.time()
            # Konverter ROUND_TIME fra minutter til sekunder ved beregning
            time_left = max(0, (ROUND_TIME * 60) - (now - round_start_time))
            current_time = pygame.time.get_ticks()
            
            # Tjek om tiden er udløbet
            if time_left <= 0 and not waiting_for_respawn and not showing_round_start:
                waiting_for_respawn = True
                respawn_timer = current_time
                
                # Afgør vinderen baseret på skade
                if spiller1.damage < spiller2.damage:
                    # Spiller 1 vinder (mindst skade)
                    spiller1.points += 1
                    round_winner = "red"
                    display_round_winner(window, "Rød Spiller", RED)
                elif spiller2.damage < spiller1.damage:
                    # Spiller 2 vinder (mindst skade)
                    spiller2.points += 1
                    round_winner = "blue"
                    display_round_winner(window, "Blå Spiller", BLUE)
                else:
                    # Uafgjort - begge får et point
                    spiller1.points += 1
                    spiller2.points += 1
                    round_winner = "tie"
                    display_round_winner(window, "Uafgjort!", WHITE)
                
                # Tjek om spillet er slut
                if spiller1.points >= MAX_POINTS or spiller2.points >= MAX_POINTS:
                    state = GameState.GAME_OVER
                    winner_name = "Rød Spiller" if spiller1.points > spiller2.points else "Blå Spiller"
                    winner_color = RED if spiller1.points > spiller2.points else BLUE
                    display_game_winner(window, winner_name, winner_color)
            
            # Tegn banen med spillernes skadeprocent
            bane.draw(window, spiller1, spiller2)
            
            # Opdater kun spillere hvis ikke viser rundestart
            if not showing_round_start:
                # Opdater spillere
                if not spiller1.is_dead:
                    spiller1.move(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
                if not spiller2.is_dead:
                    spiller2.move(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
                
                # Tjek for fald i afgrunden
                if not waiting_for_respawn:  # Tjek kun for fald hvis runden ikke er slut
                    if not spiller1.is_dead and spiller1.body.top > platform.y:  # Hvis spiller er under platformen
                        spiller1.is_dead = True
                        if first_to_fall is None:
                            first_to_fall = 1
                    
                    if not spiller2.is_dead and spiller2.body.top > platform.y:  # Hvis spiller er under platformen
                        spiller2.is_dead = True
                        if first_to_fall is None:
                            first_to_fall = 2
                
                # Opdater spillere
                if not spiller1.is_dead:
                    spiller1.update(platform)
                if not spiller2.is_dead:
                    spiller2.update(platform)
                
                # Håndter kollisioner hvis begge spillere er i live
                if not spiller1.is_dead and not spiller2.is_dead:
                    handle_collision(spiller1, spiller2, punch_sound)
                
                # Tjek for rundens afslutning
                if not waiting_for_respawn and (spiller1.is_dead or spiller2.is_dead):
                    waiting_for_respawn = True
                    respawn_timer = current_time
                    
                    # Tildel point baseret på hvem der faldt først
                    if first_to_fall == 1:  # Rød faldt først, Blå vinder
                        spiller2.points += 1
                        round_winner = "blue"
                        display_round_winner(window, "Blå Spiller", BLUE)
                    elif first_to_fall == 2:  # Blå faldt først, Rød vinder
                        spiller1.points += 1
                        round_winner = "red"
                        display_round_winner(window, "Rød Spiller", RED)
                    else:  # Hvis ingen er faldet endnu, men nogen er død
                        if spiller1.is_dead:  # Rød er død, Blå vinder
                            spiller2.points += 1
                            round_winner = "blue"
                            display_round_winner(window, "Blå Spiller", BLUE)
                        else:  # Blå er død, Rød vinder
                            spiller1.points += 1
                            round_winner = "red"
                            display_round_winner(window, "Rød Spiller", RED)
                    
                    # Nulstil first_to_fall til næste runde men behold styr på hvem der vandt
                    first_to_fall = None
                    
                    # Tjek om spillet er slut
                    if spiller1.points >= MAX_POINTS or spiller2.points >= MAX_POINTS:
                        state = GameState.GAME_OVER
                        winner_name = "Rød Spiller" if spiller1.points > spiller2.points else "Blå Spiller"
                        winner_color = RED if spiller1.points > spiller2.points else BLUE
                        display_game_winner(window, winner_name, winner_color)
            
            # Håndter respawn timing
            if waiting_for_respawn and current_time - respawn_timer >= RESPAWN_DELAY:
                waiting_for_respawn = False
                round_num += 1
                round_start_time = time.time()
                reset_round()
            
            # Tegn spillere
            spiller1.draw(window)
            spiller2.draw(window)
            
            # Tegn UI ovenpå
            display_points(window, spiller1, spiller2, time_left)
            
            # Vis rundestart display
            if showing_round_start:
                display_round_start(window, round_num)
                if current_time - round_start_display_timer >= ROUND_START_DELAY:
                    showing_round_start = False
            
            # Hvis venter på respawn, fortsæt med at vise vinder besked
            elif waiting_for_respawn:
                if round_winner == "blue":
                    display_round_winner(window, "Blå Spiller", BLUE)
                elif round_winner == "red":
                    display_round_winner(window, "Rød Spiller", RED)
        
        elif state == GameState.GAME_OVER:
            # Tegn banen som baggrund
            bane.draw(window)
            spiller1.draw(window)
            spiller2.draw(window)
            display_points(window, spiller1, spiller2, time_left)
            winner_name = "Rød Spiller" if spiller1.points > spiller2.points else "Blå Spiller"
            winner_color = RED if spiller1.points > spiller2.points else BLUE
            display_game_winner(window, winner_name, winner_color)
            
            # Tjek for nyt spil eller returner til menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Ryd ressourcer
                        pygame.mixer.music.stop()
                        pygame.quit()
                        # Genstart spillet
                        python = sys.executable
                        os.execl(python, python, *sys.argv)
                    elif event.key == pygame.K_ESCAPE:
                        # Returner til hovedmenu
                        state = GameState.MENU
                        spiller1.points = 0
                        spiller2.points = 0
                        reset_round()
                        round_num = 1
                        round_start_time = time.time()
                        pygame.mixer.music.play(-1)  # Genoptag menu musik
        
        elif state == GameState.PAUSE:
            # Tegn banen som baggrund for pause skærm
            bane.draw(window)
            spiller1.draw(window)
            spiller2.draw(window)
            display_points(window, spiller1, spiller2, time_left)
            
            # Vis pause skærm
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