# Window settings
WIDTH = 1200  # Increased from 800
HEIGHT = 800  # Increased from 600
FRAME_RATE = 60

# Colors in RGB format
WHITE = (255, 255, 255)
RED = (220, 60, 60)       # More muted red
BLUE = (60, 60, 220)      # More muted blue
GREEN = (60, 179, 113)    # More pleasant green
BLACK = (30, 30, 30)      # Softer black
GRAY = (128, 128, 128)    # For UI elements
GOLD = (212, 175, 55)     # For victory effects

# Physics settings
GRAVITY = 0.6             # Faster fall
JUMP_FORCE = -12          # Stronger jump
MOVEMENT_SPEED = 6        # Faster base movement
AIR_RESISTANCE = 0.95     # More air control
FRICTION = 0.85           # Same friction

# Combat settings
BASE_KNOCKBACK = 8        # Base knockback
MAX_KNOCKBACK = 40        # Higher max knockback
PLAYER_SIZE = 30          # Slightly larger players
DAMAGE_AMOUNT = 6         # Base damage
MAX_DAMAGE = 100          # Max damage percent
RECOVERY_FRAMES = 15      # Frames where you can't take damage after hit

# Dash settings
DASH_FORCE = 18           # Dash force
DASH_LENGTH = 10          # Dash length
DASH_COOLDOWN = 240       # 4 seconds between each dash (FPS * 4)
DASH_DAMAGE_BONUS = 1.8   # Damage bonus when dashing
MAX_AIR_DASH = 1          # Keep one air dash

# Platform settings
PLATFORM_X = WIDTH * 0.15  # Platform position scales with new width
PLATFORM_Y = HEIGHT * 0.6  # Platform is higher up to make void bigger
PLATFORM_WIDTH = WIDTH * 0.7  # Platform width scales with new width
PLATFORM_HEIGHT = 20  # Keep same height

# Spawn settings
SPAWN_DISTANCE = 100  # Increased from 50 for wider platform
SPAWN_HEIGHT = 200  # Increased from 150 for higher spawns

# Game settings
ROUND_TIME = 60           # 1 min per round
MAX_POINTS = 3            # Points needed to win

# UI settings
LARGE_FONT = 48           # Large headers
MEDIUM_FONT = 36          # Medium text
SMALL_FONT = 24           # Small text 