#
#
#      ______         __                            __                  _______                       __
#     /      \       /  |                          /  |                /       \                     /  |
#    /$$$$$$  |      $$ |____    ______    _______ $$/   _______       $$$$$$$  |  ______    _______ $$/  _______    ______          ______    ______   _____  ____    ______
#    $$ |__$$ |      $$      \  /      \  /       |/  | /       |      $$ |__$$ | /      \  /       |/  |/       \  /      \        /      \  /      \ /     \/    \  /      \
#    $$    $$ |      $$$$$$$  | $$$$$$  |/$$$$$$$/ $$ |/$$$$$$$/       $$    $$<  $$$$$$  |/$$$$$$$/ $$ |$$$$$$$  |/$$$$$$  |      /$$$$$$  | $$$$$$  |$$$$$$ $$$$  |/$$$$$$  |
#    $$$$$$$$ |      $$ |  $$ | /    $$ |$$      \ $$ |$$ |            $$$$$$$  | /    $$ |$$ |      $$ |$$ |  $$ |$$ |  $$ |      $$ |  $$ | /    $$ |$$ | $$ | $$ |$$    $$ |
#    $$ |  $$ |      $$ |__$$ |/$$$$$$$ | $$$$$$  |$$ |$$ \_____       $$ |  $$ |/$$$$$$$ |$$ \_____ $$ |$$ |  $$ |$$ \__$$ |      $$ \__$$ |/$$$$$$$ |$$ | $$ | $$ |$$$$$$$$/
#    $$ |  $$ |      $$    $$/ $$    $$ |/     $$/ $$ |$$       |      $$ |  $$ |$$    $$ |$$       |$$ |$$ |  $$ |$$    $$ |      $$    $$ |$$    $$ |$$ | $$ | $$ |$$       |
#    $$/   $$/       $$$$$$$/   $$$$$$$/ $$$$$$$/  $$/  $$$$$$$/       $$/   $$/  $$$$$$$/  $$$$$$$/ $$/ $$/   $$/  $$$$$$$ |       $$$$$$$ | $$$$$$$/ $$/  $$/  $$/  $$$$$$$/
#                                                                                                                  /  \__$$ |      /  \__$$ |
#                                                                                                                  $$    $$/       $$    $$/
#                                                                                                                   $$$$$$/         $$$$$$/
# Copyright 2024 Alexander Baranov
# Protected by the Apache License 2.0
#
#
import pygame
import random
from data.logo import logo

pygame.init()
print(logo)

car1 = pygame.image.load("textures/blue.png")
car2 = pygame.image.load("textures/green.png")
car3 = pygame.image.load("textures/yellow.png")
many_cars = [pygame.transform.scale(car1, (car1.get_width() * 2, car1.get_height() * 2)),
             pygame.transform.scale(car2, (car2.get_width() * 2, car2.get_height() * 2)),
             pygame.transform.scale(car3, (car3.get_width() * 2, car3.get_height() * 2))]

road = pygame.image.load("textures/main/road.png")
player = pygame.image.load("textures/main/red.png")
player = pygame.transform.scale(player, (player.get_width() * 2, player.get_height() * 2))

width = 584
height = 800
screen = pygame.display.set_mode((width, height))

road_pos = 0
road_height = 800
speed = 2
min_speed = 1.5
max_speed = 5.5

player_x = 194.66
target_x = 194.66
y = 600
slide_speed = 3

y_gen = 0
cars = []
points = 0

try:
    font = pygame.font.Font("data/PressStart2P-Regular.ttf", 30)
except FileNotFoundError:
    font = pygame.font.Font(None, 8)

best_score = 0
try:
    with open("data/best_score.txt", "r") as file:
        best_score = int(file.read())
except FileNotFoundError:
    pass


class MovingCar:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw_car(self):
        self.y += speed
        screen.blit(self.color, (self.x, self.y))


def draw_score_box(points, best_score):
    box_width, box_height = 250, 80
    box_x = (width - box_width) // 2
    box_y = 10
    pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)
    score_text = font.render(f"Score: {points}", True, (255, 255, 255))
    best_score_text = font.render(f"Best: {best_score}", True, (255, 255, 255))
    total_height = sum([score_text.get_height(), best_score_text.get_height()])
    vertical_padding = (box_height - total_height) // 4
    screen.blit(score_text, (box_x + (box_width - score_text.get_width()) // 2, box_y + vertical_padding))
    screen.blit(best_score_text, (box_x + (box_width - best_score_text.get_width()) // 2,
                                  box_y + vertical_padding + score_text.get_height()))


run = True
while run:
    road_pos += speed
    if road_pos >= road_height:
        road_pos = 0
    screen.blit(road, (0, road_pos))
    screen.blit(road, (0, road_pos - road_height))
    y_gen += 1
    if y_gen >= 400:
        lane = random.randint(0, 2)
        lane_positions = [0, 194.66, 389.33]
        car_x = lane_positions[lane]
        car = MovingCar(car_x, -200, random.choice(many_cars))
        cars.append(car)
        y_gen = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                target_x -= 194.66
            elif event.key == pygame.K_d:
                target_x += 194.66
            elif event.key == pygame.K_w:
                speed = min(speed + 0.5, max_speed)
            elif event.key == pygame.K_s:
                speed = max(speed - 0.5, min_speed)
    if target_x < 0:
        target_x = 0
    elif target_x > 389.33:
        target_x = 389.33
    if player_x < target_x:
        player_x += slide_speed
        if player_x > target_x:
            player_x = target_x
    elif player_x > target_x:
        player_x -= slide_speed
        if player_x < target_x:
            player_x = target_x
    screen.blit(player, (player_x, y))
    for i in cars[:]:
        i.draw_car()
        if y - 75 < i.y < y + 75 and abs(player_x - i.x) < 100:
            restart = True
            cars.clear()
            while restart:
                screen.fill((0, 0, 0))
                font = pygame.font.Font("data/PressStart2P-Regular.ttf", 24)
                text1 = font.render('YOU CRASHED!', True, (255, 255, 255))
                text2 = font.render(f'Points: {points}', True, (255, 255, 255))
                text3 = font.render(f'Best score: {best_score}', True, (255, 255, 255))
                text4 = font.render('Press "R" to restart', True, (255, 255, 255))
                screen.blit(text1, (35, 150))
                screen.blit(text2, (40, 190))
                screen.blit(text3, (40, 230))
                screen.blit(text4, (40, 270))
                pygame.display.update()
                if points > best_score:
                    best_score = points
                    with open("data/best_score.txt", "w") as file:
                        file.write(str(best_score))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        restart = False
                        run = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        restart = False
                        points = 0
                        speed = 2
        if i.y > height:
            cars.remove(i)
            points += 1
    draw_score_box(points, best_score)
    pygame.display.update()
    screen.fill((0, 0, 0))

pygame.quit()
