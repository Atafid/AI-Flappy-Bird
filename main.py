import pygame as py
import random as rd
from src.parameters import *
from src.game import *
from pipes import *
from src.ia import *

human = False
simu = Simulation(BIRD_NUMBER, human)

fps = 30

quit = False
has_began = False

human_changed = False

while (not (has_began) and not (quit)):
    py.time.delay(fps)

    for e in py.event.get():
        if (e.type == py.QUIT):
            quit = True

    keys = py.key.get_pressed()

    if (keys[py.K_SPACE]):
        has_began = True

        if (human):
            simu = Simulation(1, human)

    if ((keys[py.K_LEFT] or keys[py.K_RIGHT]) and not (human_changed)):
        human = not (human)
        human_changed = True

    if (not (keys[py.K_LEFT]) and not (keys[py.K_RIGHT])):
        human_changed = False

    simu.game.display_start_menu(not (human))

    py.display.update()


while (not (quit)):
    py.time.delay(fps)

    for e in py.event.get():
        if (e.type == py.QUIT):
            quit = True

    keys = py.key.get_pressed()

    if (not (human)):
        if (keys[py.K_RIGHT] and fps > 1):
            fps -= 1

        if (keys[py.K_LEFT]):
            fps += 1

    simu.update(keys, fps)

    py.display.update()

py.quit()
