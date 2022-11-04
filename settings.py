from math import pi, tan

RES = WIDTH, HEIGHT = 1280, 720
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
TILEPX = 80    # 16x9 grid
FPS = 60

# movement - see also '_tutorial/player-movement.jpg'
PLAYER_POS = 1.5, 5 # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
    # to eliminate pixelation on close-up we need to give player a non-pointlike size
    # (something, something avoiding large numbers in trig) 
PLAYER_SIZE_SCALE = 60

# raycasting - see '_tutorial/raycasting-settings.jpg'
FOV = pi / 3    # 60deg
HALF_FOV = FOV / 2    # 30deg
NUM_RAYS = WIDTH // 2    # large but arbitrary
DELTA_ANGLE = FOV / NUM_RAYS    # angle between rays
MAX_DEPTH = 20   # limit how many grid intersections to project (per x, y-axis)

# projection - see 'raycasting-projection-topdown.jpg'
SCREEN_DIST = HALF_WIDTH / tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

# texturing
TEXTURE_SIZE = 256  # px
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2