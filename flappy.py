import pygame, sys, random #sys give us acces to sytem modules

def draw_floor():
    screen.blit(floor_surface, (floor_x_position, 900))
    # this puts another floor in the right of the previous one 
    screen.blit(floor_surface, (floor_x_position + 576, 900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    botton_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))#made pipe spawn off screen
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    
    return botton_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5 #move pipes a little bit to left
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:#if the pipe is on botton
            screen.blit(pipe_surface, pipe)
        else: #if not flips the top pipe on the y axes, if second bool was true it would flip in x
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)
# stops the game if hit something
def check_collision(pipes):
    for pipe in pipes:
        # checks if the rectangles are colliding
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
        # check if it go too far above or if it hit the floor
        if bird_rect.top <= -100 or bird_rect.bottom >= 900:
            
            return False
    return True

def rotate_bird(bird):
    # roto zoom can rotate and zoom dempending on the last argument
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255)) #white rgb
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))#white rgb
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255)) 
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)
        
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()#for fps
# background
bg_surface = pygame.image.load('assets/sprites/background-day.png').convert()#it make it easier to run the game
# adjust the image to the screen, doubling it in size
bg_surface = pygame.transform.scale2x(bg_surface)
# floor
floor_surface = pygame.image.load('assets/sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0
# font
game_font = pygame.font.Font('04B_19.ttf',40)

# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
# bird
# convert_alpha deletes de black squere
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)
# bird_surface = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center=(100,512))#puts a rectangle around the bird
# PIPES
pipe_surface = pygame.image.load('assets/sprites/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# SPAWN a pipe every second(trigger by a timer)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)#1,2 seconds
pipe_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/sprites/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288,512))

flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
death_sound = pygame.mixer.Sound('assets/audio/hit.wav')
score_sound = pygame.mixer.Sound('assets/audio/point.wav')
score_sound_countdown = 100
while True:
    # pygame looks for all the events that are happening like moving the mouse
    for event in pygame.event.get():
        # this is for closing the game window 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # event to check if key was press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0 #disable all the effects of gravity before jump
                bird_movement -= 4 # to move the bird we made it negative numbers
                # flap sound
            flap_sound.play()
            # triggers spawn pipe
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                score = 0

        if event.type == SPAWNPIPE:
            # extend the list with what is return from argument which is a tuple
            pipe_list.extend(create_pipe())
        # flaps
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index +=1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()

    # put one surface in another surface
    screen.blit(bg_surface, (0, 0))
    if game_active:
        
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        # add bird rectangle to the image
        screen.blit(rotated_bird, bird_rect)
        game_active=check_collision(pipe_list)
        
        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    floor_x_position -= 1 #moves the floor 
    draw_floor()
        


    # moves the floor to the right again when the screen surface is over
    if floor_x_position <= -576:
        floor_x_position = 0

    
    

    pygame.display.update()
    clock.tick(120)#its never going faster that 120fps
