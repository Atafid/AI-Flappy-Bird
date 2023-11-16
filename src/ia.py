from src.game import *
from src.parameters import *
from src.bird import *
from src.game import *
from src.functions import *

import pygame as py


class Simulation():
    def __init__(self, bird_number, human_play):
        self.bird_number = bird_number
        self.game = Game(bird_number, human_play)

        self.human_play = human_play

        self.fittest_bird = None
        self.best_fitness = 0
        self.first_bird_network = None

        self.fitness = 0
        self.highscore = 0
        self.generation = 1

        self.disp_information = False
        self.information_changed = False

        self.font = py.font.Font(FONT, FONT_SIZE)

    def update(self, keys, fps):
        self.game.update(keys)

        if (not (self.human_play)):
            self.handle_keys(keys)

            if (self.disp_information):
                self.disp_informations(fps)

            if (not (self.game.is_active)):
                self.fitness = 0
                self.mutate()

            self.fitness += 0.01

            self.game.fitness = self.fitness

        if (self.game.score > self.highscore):
            self.highscore = self.game.score

    def handle_keys(self, keys):
        if (keys[py.K_d] and not (self.information_changed)):
            self.disp_information = not (self.disp_information)
            self.information_changed = True

        if (not (keys[py.K_d])):
            self.information_changed = False

        if (keys[py.K_p] and not (self.game.parameters_changed)):
            self.game.disp_parameters = not (self.game.disp_parameters)
            self.game.parameters_changed = True

        if (not (keys[py.K_p])):
            self.game.parameters_changed = False

    def get_best_bird(self):
        fitnesses = [(bird.fitness, bird) for bird in self.game.bird]
        fitnesses.sort(key=firstElement)

        if (fitnesses[-1][0] > self.best_fitness):
            self.fittest_bird = fitnesses[-1][1]
            self.best_fitness = fitnesses[-1][0]

        return (fitnesses[-1][1], fitnesses[-2][1])

    def clone_bird(self, bird):
        clone = Bird()

        for i in range(len(clone.network.layers)):
            clone.network.layers[i].weights = np.copy(
                bird.network.layers[i].weights)
            clone.network.layers[i].bias = np.copy(bird.network.layers[i].bias)

        return (clone)

    def average_bird(self, first_bird, second_bird):
        average_bird = Bird()

        for i in range(len(average_bird.network.layers)):
            average_bird.network.layers[i].weights = np.copy(
                (first_bird.network.layers[i].weights + second_bird.network.layers[i].weights)/2)
            average_bird.network.layers[i].bias = np.copy(
                (first_bird.network.layers[i].bias + second_bird.network.layers[i].bias)/2)

        return (average_bird)

    def get_clones(self, bird):
        clones = []

        for i in range(self.bird_number//3):
            clone = self.clone_bird(bird)
            clone.network.mutate()

            clones.append(clone)

        return (clones)

    def get_average(self, first_bird, second_bird):
        new_birds = []
        average = self.average_bird(first_bird, second_bird)

        for i in range(self.bird_number//3):
            clone_average = self.clone_bird(average)
            clone_average.network.mutate()

            new_birds.append(clone_average)

        return (new_birds)

    def mutate(self):
        first_bird, second_bird = self.get_best_bird()
        self.first_bird_network = first_bird.network

        first_bird_clones = self.get_clones(first_bird)
        second_bird_clones = self.get_clones(second_bird)
        average_two_birds = self.get_average(first_bird, second_bird)

        new_birds = first_bird_clones+second_bird_clones + \
            average_two_birds+[first_bird, self.fittest_bird]

        self.generation += 1
        self.game.replay(bird=new_birds)

    def get_bird_alive(self):
        bird_alive = 0

        for bird in self.game.bird:
            if (not (bird.dead)):
                bird_alive += 1

        return (bird_alive)

    def disp_informations(self, fps):

        show_text("fitness : "+str(round(self.fitness, 2)), self.font,
                  FONT_COLOR, TEXT_X, TEXT_Y, self.game.window)
        show_text("highscore : "+str(self.highscore), self.font,
                  FONT_COLOR, TEXT_X, TEXT_Y+FONT_SIZE, self.game.window)
        show_text("birds alive : "+str(self.game.bird_alive), self.font,
                  FONT_COLOR, TEXT_X, TEXT_Y+2*FONT_SIZE, self.game.window)
        show_text("generation : "+str(self.generation), self.font,
                  FONT_COLOR, TEXT_X, TEXT_Y+3*FONT_SIZE, self.game.window)
        show_text("fps : "+str(round(60/fps, 2)), self.font, FONT_COLOR,
                  TEXT_X, TEXT_Y+4*FONT_SIZE, self.game.window)
        show_text(INFO_TEXT, self.font, FONT_COLOR, TEXT_X,
                  TEXT_Y+5*FONT_SIZE, self.game.window)
        show_text(INFO_TEXT2, self.font, FONT_COLOR, TEXT_X,
                  TEXT_Y+6*FONT_SIZE, self.game.window)

        if (self.first_bird_network == None):
            draw_network(self.game.bird[0].network, self.game.window, X_NETWORK,
                         Y_NETWORK, RADIUS_NEURONS, SPACE_NETWORK)

        else:
            draw_network(self.first_bird_network, self.game.window,
                         X_NETWORK, Y_NETWORK, RADIUS_NEURONS, SPACE_NETWORK)
