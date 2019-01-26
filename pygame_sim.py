""""
RBE_ARN Homework 1
WPI MS Robotics engineering
Ryan Ferrin
2019/01/27
Simple Reactive navigation:
This code is a simulation of a "roomba" style robot that only changes direction when it encounters an obstacle.
the code displays the current absolute position, absolute orientation in degrees, relative translation, 
and relative rotation on the bottom of the screen. The Robot path trace can be toggled on and off by changing 
trace to True or False. The position data is saved to a text file 'ARN_HW1.txt'
python version 3.6.7

"""

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

# read obstacle map and build an array of obstacle nodes
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

# define variables used track robot position and heading
bot_rad = 14
bot_pos = (20, rows-20)
bot_angle = 2 * math.pi
scan_rad = 4
bot_move = 2
pos_prior = bot_pos
rotation = 0


# function to define a line to represent robot front
def line_end(bot_pos, bot_rad, bot_angle):
    le_x = int(bot_pos[0] + bot_rad * math.cos(bot_angle))
    le_y = int(bot_pos[1] + bot_rad * math.sin(bot_angle))
    bot_lend = (le_x, le_y)
    return bot_lend

bot_lend = line_end(bot_pos, bot_rad, bot_angle)


# function used to detect if robot collided with an undetected obstacle.
def collision_detect(bot_rad, bot_pos, bot_angle, obs_loc):
    i = bot_angle
    for a in range(0, 12):
        c_x = int(bot_pos[0] + bot_rad * math.cos(i))
        c_y = int(bot_pos[1] + bot_rad * math.sin(i))
        if (c_x, c_y) in obs_loc:
            return True
        i = i - math.pi / 6
    return False


# funtion to detect obsticals in front of the robot
def obs_detect(bot_rad, bot_pos, bot_angle, obs_loc):
    i = bot_angle + math.pi / 4
    obs_scan = math.sqrt(2 * bot_rad**2)
    for a in range(0, 3):
        sen_loc_x = int(bot_pos[0] + obs_scan * math.cos(i))
        sen_loc_y = int(bot_pos[1] + obs_scan * math.sin(i))
        if (sen_loc_x, sen_loc_y) in obs_loc:
            return True
        i = i - math.pi / 4
    return False

# function to find open paths"
def scan_area(bot_rad, scan_rad, bot_pos, bot_angle, obs_loc):
    a = bot_angle - math.pi / 4
    b = bot_angle + math.pi / 4
    free = []
    for x in range(0, 2):
        sen_xa = int(bot_pos[0] + (bot_rad + scan_rad) * math.cos(a))
        sen_ya = int(bot_pos[1] + (bot_rad + scan_rad) * math.sin(a))
        sen_xb = int(bot_pos[0] + (bot_rad + scan_rad) * math.cos(b))
        sen_yb = int(bot_pos[1] + (bot_rad + scan_rad) * math.sin(b))
        if (sen_xa, sen_ya) not in obs_loc:
            free.append(a)
        if (sen_xb, sen_yb) not in obs_loc:
            free.append(b)
        a = a - math.pi / 4
        b = b + math.pi / 4

    if len(free) == 0:
        free.append(bot_angle - math.pi)
    if len(free) == 1:
        new_angle = free[0]
    else:
        new_angle = free[random.randint(0, len(free) - 1)]
    return new_angle



def main(bot_rad, bot_pos, bot_angle, obs_loc, bot_lend):

#initialize and prepare pygame screen for simulation

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(win_size)
    pygame.display.set_caption('Roomba Sim')
    background = pygame.image.load("Obs_hw1.png")
    screen.blit(background, (0, 0))
    pygame.draw.circle(screen, red, bot_pos, bot_rad, 10)
    pygame.draw.line(screen, green, bot_pos, bot_lend, 4)
    font = pygame.font.SysFont("monospace", 16)
    traker = pygame.Surface((columns, 50))
    screen.blit(traker, (0, rows+1))
    pygame.display.update()

    file = open('ARN_HW1.txt', 'w')

    trace = False
    running = True
    rotation = 0
    while running:
        #Check for obstacles and move robot
        collision = collision_detect(bot_rad, bot_pos, bot_angle, obs_loc)

        if collision:
            print("collision")
            pos_prior = bot_pos
            bot_pos_x = int(bot_pos[0] - 4 * bot_move * math.cos(bot_angle))
            bot_pos_y = int(bot_pos[1] - 4 * bot_move * math.sin(bot_angle))
            bot_pos = (bot_pos_x, bot_pos_y)
            bot_lend = line_end(bot_pos, bot_rad, bot_angle)
            translation = numpy.subtract(bot_pos, pos_prior)
            ang_prior = bot_angle
            bot_angle = scan_area(bot_rad, scan_rad, bot_pos, bot_angle, obs_loc)
            if bot_angle > 2 * math .pi:
                bot_angle = bot_angle - 2 * math.pi
            if bot_angle < 0:
                bot_angle = 2 * math.pi + bot_angle
            rotation = bot_angle - ang_prior
        else:
            obs = obs_detect(bot_rad, bot_pos, bot_angle, obs_loc)
            if obs:
                print("obstacle")
                ang_prior = bot_angle
                bot_angle = scan_area(bot_rad, scan_rad, bot_pos, bot_angle, obs_loc)
                if bot_angle > 2 * math.pi:
                    bot_angle = bot_angle - 2 * math.pi
                if bot_angle < 0:
                    bot_angle = 2 * math.pi + bot_angle
                rotation = bot_angle - ang_prior

            else:
                pos_prior = bot_pos
                bot_pos_x = int(bot_pos[0] + bot_move * math.cos(bot_angle))
                bot_pos_y = int(bot_pos[1] + bot_move * math.sin(bot_angle))
                bot_pos = (bot_pos_x, bot_pos_y)
                bot_lend = line_end(bot_pos, bot_rad, bot_angle)
                translation = numpy.subtract(bot_pos, pos_prior)
        # update pygame screen
        if not trace:
            screen.blit(background, (0, 0))
        pygame.draw.circle(screen, red, bot_pos, bot_rad, 10)
        pygame.draw.line(screen, blue, bot_pos, bot_lend, 4)
        screen.blit(traker, (0, rows + 1))
        pos_text = font.render("Position " + str(bot_pos), True, yellow)
        ang_text = font.render("Orientation " + str(bot_angle * 180 / math.pi), True, yellow)
        trnl_text = font.render("Translation " + str(translation), True, yellow)
        rot_text = font.render("Rotation " + str(rotation * 180 / math.pi), True, yellow)
        screen.blit(pos_text, (0, rows + pos_text.get_height() // 2))
        screen.blit(ang_text, (0, rows + pos_text.get_height() + 4))
        screen.blit(trnl_text, (columns / 2, rows + pos_text.get_height() // 2))
        screen.blit(rot_text, (columns / 2, rows + pos_text.get_height() + 4))

        # write data to file.
        print("postion ", bot_pos, "angle ", bot_angle)
        file = open('ARN_HW1.txt', 'a')
        file.write("Position " + repr(bot_pos) + " Translation " + repr(translation) + " Orientation " + repr(bot_angle * 180 / math.pi) + " Rotation " + repr(rotation * 180 / math.pi) + '\n')
        file.close()
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == '__main__':
    main(bot_rad, bot_pos, bot_angle, obs_loc, bot_lend)





