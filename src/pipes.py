from src.parameters import *
import pygame as py
import random as rd


class Pipes():
    def __init__(self):

        PIPES_APP = [py.image.load(
            "ressources/sprites/pipe-green.png").convert_alpha(), py.image.load(
            "ressources/sprites/pipe-red.png").convert_alpha()]

        appearance = rd.randint(0, 1)

        self.app_top = PIPES_APP[appearance]
        self.app_top = py.transform.flip(self.app_top, False, True)

        self.app_bottom = PIPES_APP[appearance]

        self.x = X_BEGIN
        self.y = rd.random()*(Y_SIZE-GROUND_SIZE+GROUND_POSITION-2*SCREEN_LIMIT)+SCREEN_LIMIT

        self.x_speed = PIPES_SPEED
        self.is_passed = False

    def update(self, game):
        self.disp(game.window)
        self.x -= self.x_speed

        if (not (self.is_passed) and self.x <= X_BIRD-PIPES_WIDTH):
            game.update_score()

    def disp(self, window):
        window.blit(self.app_bottom, (self.x, self.y))
        window.blit(self.app_top, (self.x, self.y-HOLE_SIZE - PIPES_SIZE))

    def collision_perfect(image1, image2, image1_x, image1_y, image2_x, image2_y):
        xoffset = image2_x - image1_x
        yoffset = image2_y - image1_y

        image1_mask = py.mask.from_surface(image1)
        image2_mask = py.mask.from_surface(image2)

        return (image1_mask.overlap(image2_mask, (xoffset, yoffset)) != None)

    def collision(self, bird, bird_x, bird_y, window):
        # rect_top = self.app_top.get_rect()
        # rect_bottom = self.app_bottom.get_rect()
        # rect_bird = bird.get_rect()

        # rect_bottom.move_ip(self.x, self.y)
        # rect_top.move_ip(self.x, self.y-HOLE_SIZE - PIPES_SIZE)
        # rect_bird.move_ip(bird_x, bird_y)

        # py.draw.rect(window, (255, 0, 0), rect_bird)
        # py.draw.rect(window, (0, 0, 255), rect_top)
        # py.draw.rect(window, (0, 255, 0), rect_bottom)

        # return (rect_top.colliderect(rect_bird) or rect_bottom.colliderect(rect_bird))

        x_offset_top = bird_x - self.x
        y_offset_top = bird_y - (self.y-HOLE_SIZE-PIPES_SIZE)

        x_offset_bottom = bird_x - self.x
        y_offset_bottom = bird_y - self.y

        top_mask = py.mask.from_surface(self.app_top)
        bottom_mask = py.mask.from_surface(self.app_bottom)
        bird_mask = py.mask.from_surface(bird)

        return ((top_mask.overlap(bird_mask, (x_offset_top, y_offset_top)) != None) or (bottom_mask.overlap(bird_mask, (x_offset_bottom, y_offset_bottom))))
