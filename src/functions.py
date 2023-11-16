import pygame as py
import numpy as np


def rotate_image(image, angle):

    # Get the center point of the image
    w, h = image.get_size()
    center = (w // 2, h // 2)

    # Rotate the image around the center point
    rotated_image = py.transform.rotate(image, angle)

    # Get the dimensions of the rotated image
    w, h = rotated_image.get_size()

    # Calculate the top-left corner of the rotated image
    x = center[0] - w // 2
    y = center[1] - h // 2

    # Create a blank surface to draw the rotated image onto
    rotated_surface = py.Surface((w, h), py.SRCALPHA)

    # Draw the rotated image onto the surface at the calculated position
    rotated_surface.blit(rotated_image, (x, y))

    return (rotated_surface)


def tab_number(n):
    if (n == 0):
        return ([0])

    max_pow = 0

    while (n/(10**max_pow) >= 1):
        max_pow += 1

    max_pow -= 1

    return ([n//(10**(max_pow-i))-n//(10**(max_pow-i+1))
             * 10 for i in range(max_pow+1)])


def show_text(string, font, color, x, y, window):
    text = font.render(string, False, color)
    text_rect = text.get_rect()
    text_rect.right = x
    text_rect.top = y

    window.blit(text, text_rect)
    return (None)


def draw_network(network, window, x_start, y_start, radius, space):
    max_output_size = 0

    for i in range(len(network.layers)):
        input_size, output_size = network.layers[i].weights.shape

        if (output_size > max_output_size):
            max_output_size = output_size

    for i in range(len(network.layers)):
        input_size, output_size = network.layers[i].weights.shape

        for j in range(output_size):
            py.draw.circle(window, (255, 0, 0),
                           (x_start+i*space, y_start+j*space+(max_output_size-output_size)/2*space), radius, width=1)
            if (i != 0):
                for k in range(input_size):
                    if (network.layers[i].weights[k][j] >= 0):
                        py.draw.line(window, (0, 255*abs(network.layers[i].weights[k][j]), 0), ((x_start+(i-1)*space+radius, y_start+k*space+(max_output_size -
                                                                                                                                              input_size)/2*space)), (x_start+i*space-radius, y_start+j*space+(max_output_size-output_size)/2*space))
                    else:
                        py.draw.line(window, (255*abs(network.layers[i].weights[k][j]), 0, 0), ((x_start+(i-1)*space+radius, y_start+k*space+(max_output_size -
                                                                                                                                              input_size)/2*space)), (x_start+i*space-radius, y_start+j*space+(max_output_size-output_size)/2*space))


def sigmoid(x):
    return (1/(1+np.exp(-x)))


def identity(x):
    return (x)


def firstElement(couple):
    return (couple[0])
