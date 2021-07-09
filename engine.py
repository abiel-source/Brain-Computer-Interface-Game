import pygame
import sys
import random
from bci import capture_snapshot, INLET, RESHAPE
import numpy as np
import tensorflow as tf

# UTILITY FUNCTIONS
###################
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,floor_y_pos))
    screen.blit(floor_surface, (floor_x_pos+576,floor_y_pos))

def create_double_pipe():
    random_pipe_height = random.choice(pipe_middle_heights)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_height - pipe_gap))
    return bottom_pipe, top_pipe

def create_floor_pipe():
    random_pipe_height = random.choice(pipe_floor_heights)
    floor_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_height))
    return floor_pipe

def create_ceiling_pipe():
    random_pipe_height = random.choice(pipe_ceiling_heights)
    ceiling_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_height))
    return ceiling_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_rate
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False,True)
            screen.blit(flip_pipe, pipe)

def check_pipe_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

def create_coin(coin_heights):
    random_coin_y = random.choice(coin_heights)
    new_coin_rect = coin_surface.get_rect(midtop = (700, random_coin_y))
    return new_coin_rect

def move_coins(coins):
    for coin in coins:
        coin.centerx -= coin_rate
    return coins
    
def draw_coins(coins):
    for coin in coins:
        screen.blit(coin_surface, coin)
    
def check_coin_collision(coins):
    for i in range(len(coins)):
        if bird_rect.colliderect(coins[i]):
            coin_sound.play()
            coins.pop(i)
            return coins # return immediately, otherwise collision event is queued multiple times
                         # => pop index i multiple times => IndexError
    return coins

def animate_player():
    global bird_surface, bird_surface_index
    global timer
    rate = 5

    if timer % rate == 0:
        if bird_surface_index < 2:
            bird_surface_index += 1
        else:
            bird_surface_index = 0

    timer += 1
    bird_surface = bird_surfaces[bird_surface_index]


# APPLICATION FUNCTIONS
#######################
def run_main_loop(MODEL_NAME, FPS, MAX_FREQ, DIFFICULTY):

    MODEL = tf.keras.models.load_model(MODEL_NAME)
    MODEL.predict(np.zeros((32,8,120)).reshape(RESHAPE))

    global game_active
    global gravity
    global bird_movement, up_strength
    global pipe_list, pipe_rate
    global floor_rate, floor_x_pos
    # gravity = 0.25
    # up_strength = 12
    # pipe_rate = 5
    # floor_rate = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= up_strength
                if event.key == pygame.K_SPACE and not game_active: # pressing space is the only way to restart the game
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 512)
                    bird_movement = 0
            if event.type == SPAWNPIPE:
                if DIFFICULTY == 'easy':
                    pipe_list.append(random.choice([create_floor_pipe(), create_ceiling_pipe()]))
                else:
                    pipe_list.extend(create_double_pipe())
            if event.type == BIRDUP:
                bird_movement = 0
                bird_movement -= up_strength
            if event.type == BIRDDOWN:
                bird_movement = 0
                bird_movement += up_strength


        # build EEG session data
        # snapshot = capture_snapshot(MAX_FREQ)
        snapshot = []
        for i in range(8):
            sample, timestamp = INLET.pull_sample() # use global INLET variable
            snapshot.append(sample[:MAX_FREQ])

        # model predictions
        net_input = np.array(snapshot).reshape(RESHAPE)
        net_output = MODEL.predict(net_input)   # set this in different file
        choice = np.argmax(net_output)

        if choice == 0:
            pygame.event.post(bird_down_event) # open ended in case we want some fx
        elif choice == 1:
            pygame.event.post(bird_up_event)

        # background
        screen.blit(bg_surface, (0,0))

        if game_active:
            # bird
            animate_player()
            # bird_movement += gravity
            bird_rect.centery += bird_movement
            screen.blit(bird_surface, bird_rect)
            game_active = check_pipe_collision(pipe_list)

            # pipes
            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

        # floor
        floor_x_pos -= floor_rate
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(FPS)


def run_new_data_loop(ACTION, MODEL_NAME, TOTAL_SNAPSHOTS, FPS, MAX_FREQ):

    # load our tensorflow model
    MODEL = tf.keras.models.load_model(MODEL_NAME)
    MODEL.predict(np.zeros((32,8,120)).reshape(RESHAPE))

    session = []
    global bird_surface, bird_rect, bird_movement, bird_rect
    global pipe_list, coin_list, floor_x_pos
    global game_active
    bird_center = (100,785) if (ACTION == 'up') else (100,15)
    # bird_bottom_bound = 800 if (ACTION == 'up') else 512
    bird_bottom_bound = 800 if (ACTION == 'up') else 800
    bird_rect = bird_surface.get_rect(center = bird_center)

    # MAIN LOOP
    for i in range(TOTAL_SNAPSHOTS):
        did_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= up_strength
                    did_up = True
                if event.key == pygame.K_SPACE and not game_active:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = bird_center
                    bird_movement = 0
            if event.type == SPAWNPIPE:
                if ACTION == 'up':
                    pipe_list.append(create_floor_pipe())
                else:
                    pipe_list.append(create_ceiling_pipe())
            if event.type == BIRDUP:
                bird_movement = 0
                bird_movement -= up_strength
                did_up = True
            if event.type == BIRDDOWN:
                bird_movement = 0
                bird_movement += up_strength
            if event.type == SPAWNCOIN:
                if ACTION == 'up':
                    coin_list.append(create_coin(coin_heights_high))
                else:
                    coin_list.append(create_coin(coin_heights_low))
        
        # build EEG session data
        # snapshot = capture_snapshot(MAX_FREQ)
        # session.append(snapshot)
        snapshot = []
        for i in range(8):
            sample, timestamp = INLET.pull_sample() # use global INLET variable
            snapshot.append(sample[:MAX_FREQ])
        session.append(snapshot)

        # model predictions
        net_input = np.array(snapshot).reshape(RESHAPE)
        net_output = MODEL.predict(net_input)   # set this in different file
        choice = np.argmax(net_output)

        print(net_output)

        if choice == 0:
            pygame.event.post(bird_down_event)
        elif choice == 1:
            pygame.event.post(bird_up_event)

        # background
        screen.blit(bg_surface, (0,0))

        # bird
        animate_player()                # rotate through bird_surfaces
                                        # there is no need to update bird_rect
        if bird_rect.bottom >= bird_bottom_bound:
            bird_movement = 0
            if did_up:              # bird up is stunted when bottom boundary is reached.
                                        # prevent this with flag variable to overwrite the error.
                bird_movement -= up_strength
        elif bird_rect.top <= 0:
            bird_movement = 0
            bird_movement += 1
        # else:
        #     bird_movement += gravity

        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        
        # pipes
        if not check_pipe_collision(pipe_list):
            # pygame.quit()
            # sys.exit()
            x = 0 # do nothing
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # coins
        coin_list = check_coin_collision(coin_list)
        coin_list = move_coins(coin_list)
        draw_coins(coin_list)

        # floor
        floor_x_pos -= floor_rate
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    return session


def run_base_data_loop(ACTION, TOTAL_SNAPSHOTS, FPS, MAX_FREQ):

    session = []
    global game_active
    global bird_surface, bird_movement, bird_rect
    global pipe_list, coin_list
    global floor_x_pos
    bird_center = (100,100) if (ACTION == 'up') else (100,512)
    bird_rect = bird_surface.get_rect(center = bird_center) # override some parameters

    for i in range(TOTAL_SNAPSHOTS):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= up_strength
                if event.key == pygame.K_SPACE and not game_active:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = bird_center
                    bird_movement = 0
            if event.type == SPAWNPIPE:
                pipe_list.extend(create_double_pipe())
            if event.type == BIRDUP:
                bird_movement = 0
                bird_movement -= up_strength
            if event.type == SPAWNCOIN:
                if ACTION == 'up':
                    coin_list.append(create_coin(coin_heights_high))
                else:
                    coin_list.append(create_coin(coin_heights_middle))
        
        # build EEG session data
        # session.append(capture_snapshot(MAX_FREQ))
        snapshot = []
        for i in range(8):
            sample, timestamp = INLET.pull_sample() # use global INLET variable
            snapshot.append(sample[:MAX_FREQ])
        session.append(snapshot)

        # background
        screen.blit(bg_surface, (0,0))

        # bird
        animate_player()    # rotate through bird_surfaces
                            # there is no need to update bird_rect
        if ACTION == 'up':
            if bird_rect.bottom >= 400:
                pygame.event.post(bird_up_event)
            bird_movement += gravity
            bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        
        # coins
        coin_list = check_coin_collision(coin_list)
        coin_list = move_coins(coin_list)
        draw_coins(coin_list)

        # floor
        floor_x_pos -= floor_rate
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(FPS) 

    pygame.quit()
    return session




# PYGAME VARIABLES
###############
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_active = True


# PHYSICS VARIABLES
################
# bird
gravity = 2.5
bird_movement = 0
# up_strength = 37
up_strength = 10

# floor
floor_rate = 5
floor_x_pos = 0
floor_y_pos = 900

# coin
coin_rate = 15

# pipe
pipe_rate = 15


# SURFACE VARIABLES
###################
# background surface
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# floor surface
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)

# bird surface
bird_downflap_right = pygame.transform.scale2x(pygame.image.load('assets/redbird-downflap.png').convert_alpha())
bird_midflap_right = pygame.transform.scale2x(pygame.image.load('assets/redbird-midflap.png').convert_alpha())
bird_upflap_right = pygame.transform.scale2x(pygame.image.load('assets/redbird-upflap.png').convert_alpha())
bird_surfaces = [bird_downflap_right, bird_midflap_right, bird_upflap_right]
timer = 0
bird_surface_index = 1

bird_surface = bird_surfaces[bird_surface_index]
bird_rect = bird_surface.get_rect(center = (100, 512))

# pipe surface
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# pipe heights
pipe_middle_heights = [400, 600, 800]
pipe_ceiling_heights = [200, 250, 300]
pipe_floor_heights = [700, 750, 800]

# pipe gap (for double pipes)
pipe_gap = 300

# coin surface
coin_surface = pygame.image.load('assets/coin.png').convert_alpha()
coin_surface = pygame.transform.scale(coin_surface, (30, 30))
coin_list = []

# coin heights
coin_heights_low = [790, 800, 810]
coin_heights_middle = [450, 475, 500]
coin_heights_high = [10, 20, 40, 50, 60, 70, 80, 90, 100, 110]


# AUDIO
#######
coin_sound = pygame.mixer.Sound('sound/coin.wav')


# USER EVENTS
#############
BIRDUP = pygame.USEREVENT + 0
bird_up_event = pygame.event.Event(BIRDUP)

BIRDDOWN = pygame.USEREVENT + 1
bird_down_event = pygame.event.Event(BIRDDOWN)

SPAWNPIPE = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNPIPE, 1000) # 10 'ups' in one (10-second) session

SPAWNCOIN = pygame.USEREVENT + 3
pygame.time.set_timer(SPAWNCOIN, 600)