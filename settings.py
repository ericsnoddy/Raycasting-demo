from math import pi, tan

RES = WIDTH, HEIGHT = 1360, 768
HALF_WIDTH = WIDTH // 2     # used for projection trig
HALF_HEIGHT = HEIGHT // 2   # used for projection trig - this is the game's horizon
TILEPX = 100    # 16x9 grid
FPS = 60
TIMER_MS = 60   # ms delay for repeating global signal event; used as an animation timer

# movement - see also '_tutorial/player-movement.jpg'
PLAYER_POS = 1.5, 7 # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
    # to eliminate pixelation on close-up we need to give player a non-pointlike size
    # (something, something trig - instead limit how close player can get) 
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 200
RECOVERY_DELAY = 700  # ms

# mouse control
MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# raycasting - see '_tutorial/raycasting-settings.jpg'
FOV = pi / 3    # 60deg
HALF_FOV = FOV / 2    # 30deg
NUM_RAYS = WIDTH // 2    # large but arbitrary
HALF_NUM_RAYS = WIDTH // 4
DELTA_ANGLE = FOV / NUM_RAYS    # angle between rays
MAX_DEPTH = 20   # limit how many grid intersections to project (per x, y-axis)

# projection - see 'raycasting-projection-topdown.jpg'
SCREEN_DIST = HALF_WIDTH / tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

# texturing
TEXTURE_SIZE = 256  # px
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
FLOOR_COLOR = (30, 30, 30)
DIGIT_RES = 72, 72  # digit image dimensions