import pygame as py
import numpy as np
import random as rd
from src.parameters import *
from src.functions import *
from src.neurons import *


class Bird():

    def __init__(self, is_human=False):

        BIRDS_APP = [[py.image.load("ressources/sprites/yellowbird-downflap.png").convert_alpha(),
                      py.image.load(
            "ressources/sprites/yellowbird-midflap.png").convert_alpha(),
            py.image.load("ressources/sprites/yellowbird-upflap.png").convert_alpha()],  [py.image.load("ressources/sprites/bluebird-downflap.png").convert_alpha(),
                                                                                          py.image.load(
                "ressources/sprites/bluebird-midflap.png").convert_alpha(),
            py.image.load("ressources/sprites/bluebird-upflap.png").convert_alpha()],  [py.image.load("ressources/sprites/redbird-downflap.png").convert_alpha(),
                                                                                        py.image.load(
                "ressources/sprites/redbird-midflap.png").convert_alpha(),
            py.image.load("ressources/sprites/redbird-upflap.png").convert_alpha()]]

        self.app = BIRDS_APP[rd.randint(0, 2)]

        self.rotated_app = self.app

        self.bird_y = Y_SIZE/2
        self.bird_speed = 0
        self.angle = 0

        self.animation = 0

        self.dead = False
        self.is_human = is_human

        self.fitness = 0

        self.network = Network()
        self.network.add(FCLayer(5, 5, identity, False,
                         np.identity(5), np.zeros((1, 5))))
        self.network.add(FCLayer(5, 3, sigmoid, True))
        self.network.add(FCLayer(3, 1, sigmoid, True))

    def jump(self):
        if (self.bird_speed > -5):
            self.bird_speed = -JUMP_SPEED

            self.angle = ANGLE_JUMP

    def gravity(self):
        if (self.bird_speed < 10):
            self.bird_speed += m*g

            if (self.angle > -45 and self.bird_speed > 0):
                self.angle -= ANGLE_DECREASE

    def animate(self):
        self.animation += 1
        if (self.animation > 2):
            self.animation = 0

    def disp(self, window):
        window.blit(
            self.rotated_app[self.animation], (X_BIRD, self.bird_y))

    def update(self, window, pipes):
        self.disp(window)
        self.animate()
        self.gravity()

        self.bird_y += self.bird_speed

        self.rotated_app = [rotate_image(self.app[i], self.angle)
                            for i in range(len(self.app))]

        if (not (self.is_human)):
            self.network.decision(self.get_parameters(pipes))
            if (self.network.outputs[0][0] > 0.5):
                self.jump()

        self.dead = self.end(window, pipes)

    def end(self, window, pipes):
        if (pipes.collision(self.rotated_app[self.animation], X_BIRD, self.bird_y, window)):
            return (True)

        return (self.bird_y >= Y_SIZE-GROUND_SIZE+GROUND_POSITION)

    def get_parameters(self, pipes):
        y = self.bird_y
        speed = self.bird_speed

        x_dist = abs(X_BIRD - pipes.x)
        y_dist_top = self.bird_y - (pipes.y-HOLE_SIZE)
        y_dist_bottom = pipes.y - self.bird_y

        return (np.array([y, speed, x_dist, y_dist_bottom, y_dist_top]))

    def disp_parameters(self, window, pipes):
        param = self.get_parameters(pipes)

        # py.draw.line(window, (0, 255, 0),
        #             (X_BIRD, param[0]), (X_BIRD+param[2], param[0]))

        # py.draw.line(window, (255, 0, 0),
        #             (pipes.x, param[0]), (pipes.x, param[0]-param[4]))
        py.draw.line(window, (255, 0, 0),
                     (X_BIRD, param[0]), (pipes.x, param[0]-param[4]))

        # py.draw.line(window, (0, 0, 255),
        #             (pipes.x, param[0]), (pipes.x, param[0]+param[3]))
        py.draw.line(window, (0, 0, 255),
                     (X_BIRD, param[0]), (pipes.x, param[0]+param[3]))
