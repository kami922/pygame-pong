import pygame
import random
import sys


# commenting out sound because the cause error when making it exe file with pyinstaller


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_timer
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # collisions
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        score_timer = pygame.time.get_ticks()
        player_score += 1

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        score_timer = pygame.time.get_ticks()
        opponent_score += 1

    '''making collisions more precise
        not much clear'''

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1

        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1

        elif abs(ball.bottom - player.top) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y, score_timer

    ball.center = (round(screen_width / 2), round(screen_height / 2))
    current_time = pygame.time.get_ticks()
    '''code to display timer on screen
    not working for some reason'''
    if current_time - score_timer < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (round(screen_width / 2 - 10), round(screen_height / 2 + 20)))
    if 700 < current_time - score_timer < 1400:
        number_two = game_font.render("2", False, light_grey)
        screen.blit(number_two, (round(screen_width / 2 - 10), round(screen_height / 2 + 20)))
    if 1400 < current_time - score_timer < 2100:
        number_one = game_font.render("1", False, light_grey)
        screen.blit(number_one, (round(screen_width / 2 - 10), round(screen_height / 2 + 20)))

    if current_time - score_timer < 2100:
        ball_speed_y, ball_speed_x = 0, 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_timer = None


# general setting
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

# timer
score_timer = True

# setting up the main window
screen_width = 950
screen_height = 660
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# game rectangles
'''dividing the width and height by 2 and subtracting 15 
will place it in the middile 30,30 are the size of ball
player and opponent:first 2 parameters are position and 2nd last 
parameters are size'''
ball = pygame.Rect(round(screen_width / 2 - 15), round(screen_height / 2 - 15), 30, 30)
player = pygame.Rect(round(screen_width - 20), round(screen_height / 2 - 70), 10, 140)
opponent = pygame.Rect(10, round(screen_height / 2 - 70), 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7
while True:
    # handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    if score_timer:
        ball_restart()

    ball_animation()
    player_animation()
    opponent_animation()
    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (520, 470))

    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (410, 470))

    # updating the window
    pygame.display.flip()
    clock.tick(60)
