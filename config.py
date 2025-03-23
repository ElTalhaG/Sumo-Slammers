# Af Talha og Azad (fælles kode stumper)
# Vindue indstillinger
WIDTH = 1200  # Skærmbredde i pixels
HEIGHT = 800  # Skærmhøjde i pixels
FRAME_RATE = 60  # Opdateringshastighed i billeder per sekund

# Farve konstanter i RGB format
WHITE = (255, 255, 255)  # Hvid farve
RED = (220, 60, 60)      # Dæmpet rød farve
BLUE = (60, 60, 220)     # Dæmpet blå farve
GREEN = (60, 179, 113)   # Behagelig grøn farve
BLACK = (30, 30, 30)     # Blød sort farve
GRAY = (128, 128, 128)   # Grå farve til UI elementer
GOLD = (212, 175, 55)    # Guld farve til sejrseffekter

# Fysik konstanter
GRAVITY = 0.6            # Tyngdekraft acceleration
JUMP_FORCE = -12         # Hopstyrke (negativ for opadgående kraft)
MOVEMENT_SPEED = 6       # Basis bevægelseshastighed
AIR_RESISTANCE = 0.95    # Luftmodstand multiplikator
FRICTION = 0.85         # Friktionskoefficient

# Kamp konstanter
BASE_KNOCKBACK = 8       # Basis tilbageslagskraft
MAX_KNOCKBACK = 40       # Maksimal tilbageslagskraft
PLAYER_SIZE = 30         # Spillerens størrelse i pixels
DAMAGE_AMOUNT = 6        # Basis skadesværdi
MAX_DAMAGE = 100        # Maksimal skadeprocent
RECOVERY_FRAMES = 15     # Antal frames hvor spilleren er immun efter at blive ramt

# Dash konstanter
DASH_FORCE = 18         # Dash kraftstyrke
DASH_LENGTH = 10        # Dash varighed i frames
DASH_COOLDOWN = 240     # Nedkølingstid mellem dash (4 sekunder ved 60 FPS)
DASH_DAMAGE_BONUS = 1.8  # Skadebonus ved dash angreb
MAX_AIR_DASH = 1        # Maksimalt antal luftdash

# Platform konstanter
PLATFORM_X = WIDTH * 0.15       # Platform x-position relativt til skærmbredde
PLATFORM_Y = HEIGHT * 0.6       # Platform y-position relativt til skærmhøjde
PLATFORM_WIDTH = WIDTH * 0.7    # Platformens bredde relativt til skærmbredde
PLATFORM_HEIGHT = 20            # Platformens højde i pixels

# Spawn konstanter
SPAWN_DISTANCE = 100    # Afstand fra platformens kant ved spawn
SPAWN_HEIGHT = 200      # Højde over platformen ved spawn

# Spil konstanter
ROUND_TIME = 1          # Rundevarighed i minutter
MAX_POINTS = 3          # Antal point der kræves for at vinde

# UI konstanter
LARGE_FONT = 48         # Stor skriftstørrelse til overskrifter
MEDIUM_FONT = 36        # Medium skriftstørrelse til almindelig tekst
SMALL_FONT = 24         # Lille skriftstørrelse til detaljer

# Verden grænser
WORLD_LEFT_BOUNDARY = -WIDTH    # Venstre verdensgrænse (en skærmbredde til venstre)
WORLD_RIGHT_BOUNDARY = WIDTH * 2  # Højre verdensgrænse (to skærmbredder til højre) 