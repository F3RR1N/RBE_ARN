from PIL import Image
import pygame
import math
import numpy
import random

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 175, 0)
red = (255, 0, 0)
purple = (85, 26, 139)
yellow = (255, 255, 100)

im = Image.open("Obs_hw1.png").convert("RGB")
size = im.size
columns = size[0]
rows = size[1]
win_size = [columns, rows+50]
grid = numpy.zeros((columns, rows))
obs_loc = []

for i in range(columns):
    for j in range(rows):
        value = im.getpixel((i, j))
        if value == white:
            grid[i, j] = 0
        elif value == black:
            grid[i, j] = 1
            obs_loc.append((i, j))

bot_rad = 14
bot_pos = (20, rows-20)
bot_angle = 2 * math.pi
scan_rad = 4
bot_move = 2
bot_prior = bot_pos

def line_end(bot_pos, bot_rad, bot_angle):
    le_x = int(bot_pos[0] + bot_rad * math.cos(bot_angle))
    le_y = int(bot_pos[1] + bot_rad * math.sin(bot_angle))
    bot_lend = (le_x, le_y)
    return bot_lend

bot_lend = line_end(bot_pos, bot_rad, bot_angle)


def collision_detect(bot_rad, bot_pos, bot_angle, obs_loc):
    i = bot_angle
    for a in range(0, 12):
        c_x = int(bot_pos[0] + bot_rad * math.cos(i))
        c_y = int(bot_pos[1] + bot_rad * math.sin(i))
        if (c_x, c_y) in obs_loc:
            return True
        i = i - math.pi / 6
        if i <= 0:
            i = 2 * math.pi
    return False


def obs_detect(bot_rad, bot_pos, bot_angle, obs_loc):
    i = bot_angle + math.pi / 4
    obs_scan = math.sqrt(2 * bot_rad**2)
    for a in range(0, 3):
        sen_loc_x = int(bot_pos[0] + obs_scan * math.cos(i))
        sen_loc_y = int(bot_pos[1] + obs_scan * math.sin(i))
        if (sen_loc_x, sen_loc_y) in obs_loc:
            return True
        i = i - math.pi / 4
        if i <= 0:
            i = 2 * math.pi
    return False


def scan_area(bot_rad, scan_rad, bot_pos, bot_angle, obs_loc):
    a = bot_angle - math.pi / 4
    # b = bot_angle + math.pi / 4
    free = []
    for x in range(0, 7):
    # searching = True
    # while searching:
        sen_xa = int(bot_pos[0] + (bot_rad + scan_rad) * math.cos(a))
        sen_ya = int(bot_pos[1] + (bot_rad + scan_rad) * math.sin(a))
        # sen_xb = int(bot_pos[0] + (bot_rad + scan_rad) * math.cos(b))
        # sen_yb = int(bot_pos[1] + (bot_rad + scan_rad) * math.sin(b))
        if (sen_xa, sen_ya) not in obs_loc:
            free.append(a)
        # if (sen_xb, sen_yb) not in obs_loc:
        #     free.append(b)
        # if len(free) != 0:
        #     # searching = False

        a = a - math.pi / 4
        # b = b - math.pi / 4
        # if a >= 2 * math.pi:
        #     a = 2 * math.pi
        if a <= 0:
            a = 0
    if len(free) == 1:
        new_angle = free[0]
    else:

        new_angle = free[random.randint(0, len(free) - 1)]
    return new_angle

def main(bot_rad, bot_pos, bot_angle, obs_loc, bot_lend):
#initialize and prepare screen
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(win_size)
    pygame.display.set_caption('Roomba Sim')
    background = pygame.image.load("Obs_hw1.png")
    screen.blit(background, (0, 0))
    pygame.draw.circle(screen, blue, bot_pos, bot_rad, 10)
    pygame.draw.line(screen, green, bot_pos, bot_lend, 4)
    pygame.display.update()

    trace = True
    running = True
    while running:

        collision = collision_detect(bot_rad, bot_pos, bot_angle, obs_loc)

        if collision:
            print("collision")
            bot_pos_x = int(bot_pos[0] - 3 * bot_move * math.cos(bot_angle))
            bot_pos_y = int(bot_pos[1] - 3 * bot_move * math.sin(bot_angle))
            bot_pos = (bot_pos_x, bot_pos_y)
            bot_lend = line_end(bot_pos, bot_rad, bot_angle)
            # bot_angle = bot_angle - math.pi / 4
            # if bot_angle <= 0:
            #     bot_angle = 2 * math.pi
        else:
            obs = obs_detect(bot_rad, bot_pos, bot_angle, obs_loc)
            if obs:
                print("obstacle")
                bot_angle = scan_area(bot_rad, scan_rad, bot_pos, bot_angle, obs_loc)
                if bot_angle <= 0:
                    bot_angle = 2 * math.pi
            else:
                bot_pos_x = int(bot_pos[0] + bot_move * math.cos(bot_angle))
                bot_pos_y = int(bot_pos[1] + bot_move * math.sin(bot_angle))
                bot_pos = (bot_pos_x, bot_pos_y)
                bot_lend = line_end(bot_pos, bot_rad, bot_angle)
        if not trace:
            screen.blit(background, (0, 0))
        pygame.draw.circle(screen, blue, bot_pos, bot_rad, 10)
        pygame.draw.line(screen, green, bot_pos, bot_lend, 4)
        print("postion ", bot_pos, "angle ", bot_angle)
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == '__main__':
    main(bot_rad, bot_pos, bot_angle, obs_loc, bot_lend)





