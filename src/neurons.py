import random as rd
import numpy as np
import pygame as py
from src.parameters import *


class FCLayer():
    def __init__(self, input_size, output_size, activation, random=False, weights=None, bias=None):
        self.inputs = np.zeros((1, input_size))

        if (random):
            self.weights = np.random.rand(input_size, output_size) - 0.5
            self.bias = np.random.rand(1, output_size) - 0.5
        else:
            self.set_weights(weights)
            self.set_bias(bias)

        self.outputs = np.zeros((output_size, 1))

        self.activation = activation

    def set_weights(self, weights):
        self.weights = weights

    def set_bias(self, bias):
        self.bias = bias

    def forward_propagation(self, input_data):
        self.inputs = input_data

        # print("input : ", self.inputs)
        # print("weights : ", self.weights)
        # print("bias : ", self.bias)

        self.outputs = self.activation(
            np.dot(self.inputs, self.weights)+self.bias)

    def mutate(self):
        lines, columns = self.weights.shape
        self.weights += (np.random.rand(lines, columns)*2*MUTATION_RANGE -
                         MUTATION_RANGE)*(np.random.randint(0, 2, (lines, columns)))


class Network():
    def __init__(self):
        self.layers = []

        self.outputs = None

    def add(self, layer):
        self.layers.append(layer)

    def decision(self, input_data):
        self.layers[0].set_bias(input_data)
        self.layers[0].forward_propagation(
            self.layers[0].inputs)

        for k in range(len(self.layers)-1):
            self.layers[k+1].forward_propagation(self.layers[k].outputs)

        self.outputs = self.layers[-1].outputs
        # print(input_data, " / ", self.outputs)

    def mutate(self):
        for l in self.layers:
            l.mutate()
