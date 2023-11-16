from src.parameters import *
from src.functions import *
from src.pipes import Pipes
from src.bird import *
import pygame as py


class Game():
    def __init__(self, bird_number=1, human_play=False):
        py.init()

        self.window = py.display.set_mode((X_SIZE, Y_SIZE))

        self.start_menu = py.image.load(
            "ressources/sprites/message.png").convert_alpha()

        self.background = py.image.load(
            "ressources/sprites/background-day.png").convert()
        self.ground = py.image.load("ressources/sprites/base.png").convert()

        self.ground_speed = GROUND_SPEED
        self.ground_position = 0

        self.fitness = 0
        self.score = 0
        self.score_image = [py.image.load(
            "ressources/sprites/"+str(i)+".png").convert_alpha() for i in range(10)]

        self.is_active = True
        self.game_over_image = py.image.load(
            "ressources/sprites/gameover.png").convert_alpha()

        self.human_play = human_play

        # BIRD
        self.bird_number = bird_number
        self.bird = [Bird(human_play) for i in range(bird_number)]

        self.bird_alive = 0

        self.disp_parameters = False
        self.parameters_changed = False

        # PIPES
        self.active_pipes = []
        self.passed_pipes = []
        self.timer_pipes = 0

        self.new_pipes()

    def display_start_menu(self, is_ia):
        self.disp_back()

        self.window.blit(self.start_menu, (X_SIZE/2 -
                         START_MENU_WIDTH/2, Y_SIZE/2-START_MENU_HEIGHT/2))

        self.window.blit(self.ground, (self.ground_position,
                                       Y_SIZE-GROUND_SIZE+GROUND_POSITION))

        show_text("AI : "+str(is_ia), py.font.Font(FONT, FONT_SIZE),
                  FONT_COLOR, TEXT_X, TEXT_Y, self.window)

    def update(self, keys):
        self.disp_back()

        if (self.is_active):
            self.is_active = self.handle_bird()
            self.handle_pipes()
            self.handle_ground()

            if (keys[py.K_SPACE] and self.human_play):
                for bird in self.bird:
                    bird.jump()

        else:
            if (self.human_play):
                self.disp_game_over()

                if (keys[py.K_SPACE]):
                    self.replay()

        self.disp_score()

    def handle_bird(self):
        self.bird_alive = 0

        end = True
        for bird in self.bird:
            end = end and bird.dead

            if (bird.dead and bird.fitness == 0):
                bird.fitness = self.fitness

            if (not (bird.dead)):
                self.bird_alive += 1

                bird.update(self.window, self.active_pipes[0])
                if (len(self.active_pipes) != 0 and self.disp_parameters):
                    bird.disp_parameters(self.window, self.active_pipes[0])

        return (not (end))

    def handle_pipes(self):

        for p in self.active_pipes:
            p.update(self)

        for p in self.passed_pipes:
            p.update(self)

        self.delete_pipes()
        if (self.timer_pipes > PIPES_FREQUENCY):
            self.timer_pipes = 0
            self.new_pipes()
        self.timer_pipes += 1

    def disp_back(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.background, (0, 0))

    def handle_ground(self):
        self.ground_position -= self.ground_speed
        if (self.ground_position <= -25):
            self.ground_position = 0

        self.window.blit(self.ground, (self.ground_position,
                                       Y_SIZE-GROUND_SIZE+GROUND_POSITION))

    def disp_game_over(self):
        self.window.blit(self.game_over_image,
                         (X_SIZE/2-GAME_OVER_WIDTH/2, Y_SIZE/4))
        self.window.blit(self.ground, (self.ground_position,
                                       Y_SIZE-GROUND_SIZE+GROUND_POSITION))

    def new_pipes(self):
        self.active_pipes.append(Pipes())

    def delete_pipes(self):
        if (len(self.passed_pipes) != 0 and self.passed_pipes[0].x < -PIPES_WIDTH):
            self.passed_pipes.pop(0)

    def update_score(self):
        self.score += 1

        self.active_pipes[0].is_passed = True
        self.passed_pipes.append(self.active_pipes[0])
        self.active_pipes.pop(0)

    def disp_score(self):
        score_tab = tab_number(self.score)

        for k in range(len(score_tab)):
            self.window.blit(
                self.score_image[score_tab[k]], (X_SCORE-(len(score_tab)-1-k)*LETTER_SPACE+len(score_tab)//2*LETTER_SPACE, Y_SCORE))

    def replay(self, bird=[]):
        self.ground_position = 0

        self.score = 0
        self.is_active = True

        if (bird != []):
            self.bird = bird

        else:
            self.bird = [Bird(self.human_play)
                         for i in range(self.bird_number)]

        self.active_pipes = []
        self.passed_pipes = []
        self.timer_pipes = 0

        self.new_pipes()
