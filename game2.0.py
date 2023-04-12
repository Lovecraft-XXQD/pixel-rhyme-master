import pygame
import random

# Initialize Pygame
pygame.init()


# Set up the screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))


# Set up the clock
clock = pygame.time.Clock()

# Load the music and sound effects
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.play(-1) # Play the music on loop

shot_sound = pygame.mixer.Sound("hit.mp3")
hit_sound = pygame.mixer.Sound("hit.mp3")
gameover_sound = pygame.mixer.Sound("hit.mp3")
# Adjust the sound volume
shot_sound.set_volume(0.3)
# Adjust the sound volume
hit_sound.set_volume(0.3)
# Adjust the sound volume
gameover_sound.set_volume(0.3)

# Define some colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Define the font
font = pygame.font.Font(None, 36)

# # Define the game name
game_name = ""

bullet_timer = 0

# Define the player
global player_x
global player_y
player_size = 50
player_x = (screen_width / 2) - (player_size / 2)
player_y = screen_height - player_size
player_speed = 10
player_health = 3

import pygame

def choose_music(screen):
    # 加载音乐文件列表
    music_files = ["一步之差—卡洛斯.mp3", "钟—李斯特.mp3", "恰空—巴赫.ogg","齐格飞的号角—瓦格纳.mp3","七重奏—贝多芬.ogg","美丽的罗丝玛琳—克莱斯勒.mp3"]

    # 创建字体对象
    font = pygame.font.Font("STCAIYUN.TTF", 36)

    # 循环处理事件
    while True:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    global game_state
                    game_state="play"
                    return
                elif event.key == pygame.K_1:
                    pygame.mixer.music.load(music_files[0])
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_2:
                    pygame.mixer.music.load(music_files[1])
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_3:
                    pygame.mixer.music.load(music_files[2])
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_4:
                    pygame.mixer.music.load(music_files[3])
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_5:
                    pygame.mixer.music.load(music_files[4])
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_6:
                    pygame.mixer.music.load(music_files[5])
                    pygame.mixer.music.play(-1)

        # 渲染文字和提示
        screen.fill(black)
        text = font.render("请选择游戏背景音乐：", True, white)
        screen.blit(text, (50, 50))
        text = font.render("1 - " + music_files[0], True, white)
        screen.blit(text, (50, 100))
        text = font.render("2 - " + music_files[1], True, white)
        screen.blit(text, (50, 150))
        text = font.render("3 - " + music_files[2], True, white)
        screen.blit(text, (50, 200))
        text = font.render("4 - " + music_files[3], True, white)
        screen.blit(text, (50, 250))
        text = font.render("5 - " + music_files[4], True, white)
        screen.blit(text, (50, 300))
        text = font.render("6 - " + music_files[5], True, white)
        screen.blit(text, (50, 350))
        text = font.render("按空格键完成选择", True, white)
        screen.blit(text, (50, 400))

        # 更新显示
        pygame.display.update()

def draw_player():
    pygame.draw.rect(screen, white, (player_x, player_y, player_size, player_size))

def update_player():

    keys = pygame.key.get_pressed()
    global player_x
    global player_y
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += player_speed

# Define the bullets
bullets = []
bullet_speed = 6

def create_bullet():
    bullet_x = player_x + (player_size / 2) - 5
    bullet_y = player_y - 10
    bullets.append({"x": bullet_x, "y": bullet_y})

def draw_bullet(bullet):
    pygame.draw.rect(screen, white, (bullet["x"], bullet["y"], 10, 10))

def update_bullets():
    for bullet in bullets:
        bullet["y"] -= bullet_speed

        if bullet["y"] < 0:
            bullets.remove(bullet)
        else:
            for shape in shapes:
                if bullet["y"] < shape["y"] + shape["size"] and bullet["x"] > shape["x"] and bullet["x"] < shape["x"] + shape["size"]:
                    bullets.remove(bullet)
                    shapes.remove(shape)
                    hit_sound.play()
                    global score
                    score += 1
                    global shape_sp
                    shape_sp +=0.05

# Define the shapes
shapes = []

shape_sp = 0
shape_timer = 0
shape_interval = 1000

def create_shape():
    shape_size = random.randint(20, 50)
    shape_x = random.randint(0, screen_width - shape_size)
    shape_y = -shape_size
    shape_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    shape_speed = random.uniform(1+shape_sp, 5+shape_sp)
    shapes.append({"x": shape_x, "y": shape_y, "size": shape_size, "color": shape_color, "speed": shape_speed})

def draw_shape(shape):
    pygame.draw.rect(screen, shape["color"], (shape["x"], shape["y"], shape["size"], shape["size"]))

def update_shapes():
    global player_health

    for shape in shapes:
        shape["y"] += shape["speed"]

        if shape["y"] > screen_height:
            shapes.remove(shape)
            player_health -= 1
            if player_health == 0:
                gameover_sound.play()
                game_over()

        if shape["y"] + shape["size"] > player_y and shape["x"] < player_x + player_size and shape["x"] + shape["size"] > player_x:
            shapes.remove(shape)
            player_health -= 1
            if player_health == 0:
                gameover_sound.play()
                game_over()

def draw_health():
    health_text = font.render(f"Health: {player_health}", True, red)
    screen.blit(health_text, (10, 10))

def draw_score():
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

def game_over():
    global game_state
    game_state = "gameover"

# Define the game state
game_state = "start"

# Define the game loop
def game_loop():
    global score, player_health, game_state, player_x, player_y, bullets, shapes,bullet_timer

    # Reset the game state
    score = 0
    player_health = 3
    player_x = (screen_width / 2) - (player_size / 2)
    player_y = screen_height - player_size
    bullets = []
    shapes = []
    # # Set up a bullet timer
    # bullet_timer = 0

    # Main game loop
    while True:
        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_state == "start":
                        game_state = "select_music"
                    elif game_state == "gameover":
                        pygame.quit()
                        exit()

        # Clear the screen
        screen.fill(black)

        # Update the game based on the game state
        if game_state == "start":
            font = pygame.font.Font("STCAIYUN.TTF", 32)
            # Draw the game name
            text = font.render("艺术与审美汇报展示", True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width/2, screen_height/2.5))
            screen.blit(text, text_rect)
            subtitle_text = font.render("音乐节奏大师像素版", True, (255, 255, 255))
            subtext_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(subtitle_text, subtext_rect)
        elif game_state == "select_music":
            choose_music(screen);
        elif game_state == "play":
            # Update the player
            update_player()

            # Create bullets when the space key is pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                # Check the bullet timer
                current_time = pygame.time.get_ticks()
                if current_time - bullet_timer > 100:
                    create_bullet()
                    shot_sound.play()
                    bullet_timer = current_time


            # Update the bullets
            update_bullets()

            # Create shapes at regular intervals
            global shape_timer
            shape_timer += clock.tick(30)
            if shape_timer > shape_interval:
                create_shape()
                shape_timer = 0

            # Update the shapes
            update_shapes()

            # Draw the player, bullets, shapes, health, and score
            draw_player()
            for bullet in bullets:
                draw_bullet(bullet)
            for shape in shapes:
                draw_shape(shape)
            draw_health()
            draw_score()

        elif game_state == "gameover":
            # Draw the game over message and final score
            gameover_text = font.render("Game Over!", True, red)
            score_text = font.render(f"Final Score: {score}", True, white)
            gameover_rect = gameover_text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
            score_rect = score_text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(gameover_text, gameover_rect)
            screen.blit(score_text, score_rect)

        # Update the screen
        pygame.display.flip()


# Start the game loop
game_loop()

# Quit Pygame
pygame.quit()
exit()


