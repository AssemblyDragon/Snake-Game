import pygame
from pygame import mixer
from cube import Cube
from cubes import Cubes
import random
import pickle
import os
from utils import scale_img


# Initialize6
pygame.init()
clock = pygame.time.Clock()

# Screen
screen_size = (600, 700)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snakey")
iconImg = pygame.image.load("icon_img.png")
pygame.display.set_icon(iconImg)

# Grid
number_of_rows = 10
grid_ySlab = screen_size[1] - screen_size[0]
grid_distance = int(screen_size[0]/number_of_rows)
start_pos_grid = (0, grid_ySlab)
end_pos_grid = screen_size

# Cubes
snake_color = (255, 0, 0)
snake_initial_size = 2
snake_speed = 450  # Normal = 450
snake_dir = {"x": 1, "y": 0}
snake_start_pos = (7, 6)
snake = Cubes(snake_color, screen, clock, snake_speed, snake_dir, grid_distance, grid_ySlab,
              snake_start_pos, snake_initial_size, number_of_rows)

# Food
food_color = (255, 255, 0)
food_pos = ()
foodSound = mixer.Sound("eatFood_music.wav")
food = None


def food_draw():
    global food, food_pos, food_color
    while True:
        food_pos = (random.randint(1, number_of_rows), random.randint(1, number_of_rows))
        if not collision(food_pos, snake.cubes_position):
            break
    food = Cube(food_color, screen, food_pos, grid_distance, grid_ySlab)


# Collisions
collisionSound = mixer.Sound("gameEnd_music.wav")


def collision(foodPos, snakePos):
    foodPos = tuple(foodPos)
    for pos in snakePos:
        if foodPos == pos:
            return True
    return False


# Music
mixer.music.load("background_music.wav")
mixer.music.play(-1)
sound = True
sound_full_icon = pygame.image.load("sound_full_img.png")
sound_mute_icon = scale_img(pygame.image.load("sound_mute_img.png"), 1)


def sound_print(sound_val):
    if sound_val:
        screen.blit(sound_full_icon, (300, 300))
    else:
        pass


# Score
font = pygame.font.Font("freesansbold.ttf", 40)
score_pos = (screen_size[0]/2 - screen_size[0]/10, grid_ySlab/2 - grid_ySlab/6)


def print_score():
    score = font.render("Score : " + str(snake.score), True, (0, 255, 0))
    screen.blit(score, score_pos)


# High score
def highscore_update(score=0, first=False):
    if first and not os.path.isfile("HighScores.txt"):
        f = open("HighScores.txt", "wb")
        pickle.dump([0], f)
        f.close()
        return
    elif first:
        return
    f = open("HighScores.txt", "rb")
    scores = pickle.load(f)
    f.close()
    if len(scores) < 10:
        if score in scores:
            return
        scores.append(score)
        scores = sorted(scores, reverse=True)
        f = open("HighScores.txt", "wb")
        pickle.dump(scores, f)
        f.close()
        return
    for i in range(len(scores)):
        if scores[i] == score:
            break
        if scores[i] < score:
            scores.insert(i, score)
            scores.pop()
            f = open("HighScores.txt", "wb")
            pickle.dump(scores, f)
            f.close()
            break


def display_high_score():
    f = open("HighScores.txt", "rb")
    scores = pickle.load(f)
    f.close()
    print(scores)


# Grid
def draw_grid(number, slabY, grid_dist, screenSize):
    temp_value = 0
    for i in range(number+1):
        pygame.draw.line(screen, (255, 255, 255), (0, temp_value+slabY), (screenSize[1], temp_value+slabY))
        pygame.draw.line(screen, (255, 255, 255), (temp_value, slabY), (temp_value, screenSize[1]))
        temp_value += grid_dist


# Main Loop
running = True
# highscore_update(first=True)
food_draw()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            pass

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake_dir["x"] != 1:
                snake_dir["x"] = -1
                snake_dir["y"] = 0
                snake.turn(snake_dir)

            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake_dir["x"] != -1:
                snake_dir["x"] = 1
                snake_dir["y"] = 0
                snake.turn(snake_dir)

            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and snake_dir["y"] != 1:
                snake_dir["x"] = 0
                snake_dir["y"] = -1
                snake.turn(snake_dir)

            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake_dir["y"] != -1:
                snake_dir["x"] = 0
                snake_dir["y"] = 1
                snake.turn(snake_dir)

    if collision(food.pos, snake.cubes_position):
        food_draw()
        snake.add_cube = True
        foodSound.play()

    if snake.internal_collision():
        running = False
        collisionSound.play()
        mixer.music.fadeout(30)
        pygame.time.delay(800)
        highscore_update(snake.score)
        print(snake.score)
        display_high_score()
        continue

    screen.fill((0, 0, 0))
    sound_print(sound)
    draw_grid(number_of_rows, grid_ySlab, grid_distance, screen_size)
    food.draw()
    snake.draw()
    snake.move()
    snake.forward()
    print_score()
    clock.tick(60)
    pygame.display.update()

pygame.QUIT
