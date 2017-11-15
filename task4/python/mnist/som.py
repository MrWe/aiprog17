import math
import random
import numpy as np
#import helpers as hp
from mnist.helpers import *
from itertools import product
import numexpr as ne



def run(neurons, images, lr, lr_reduction_factor, dist_threshold, neighbour_value, steps=1):

    for i in range(steps):
        random_image = random.choice(images)
        closest_neuron_x, closest_neuron_y = shortest_dist(random_image, neurons)
        update_neurons(random_image, neurons, closest_neuron_x, closest_neuron_y, lr, lr_reduction_factor, dist_threshold, neighbour_value)
    return neurons


def euclideanDistance(neuron_weights, image_pixels, classification=False):
    # if(classification):
    #     total = 0
    #     for i in range(len(neuron_weights)):
    #         if(not (neuron_weights[i] == 0) and not (image_pixels[i] == 0)):
    #             total += pow(neuron_weights[i] - image_pixels[i], 2)
    #     return pow(total,0.5)
    return np.sqrt(np.sum(np.power(np.subtract(neuron_weights, image_pixels),2)))

def squared_row_norms(X):
    # From http://stackoverflow.com/q/19094441/166749
    return np.einsum('ij,ij->i', X, X)

def squared_euclidean_distances(data, vec):
    data2 = squared_row_norms(data)
    vec2 = squared_row_norms(vec)
    d = np.dot(data, vec.T).ravel()
    d *= -2
    d += data2
    d += vec2
    return d


def shortest_dist(image_pixels, neurons):
    sh = float("inf")
    index_x = 0
    index_y = 0
    for x in range(len(neurons)):
        for y in range(len(neurons[x])):
            d = squared_euclidean_distances(image_pixels, neurons[x][y])
            if d < sh:
                sh = d
                index_x = x
                index_y = y
    return index_x, index_y

def update_neurons(image, neurons, index_x, index_y, lr, lr_reduction_factor, dist_threshold, neighbour_value):
    update_neuron(image, neurons, index_x, index_y, lr)


    for neuron in get_neighbouring_neurons(image, index_x, index_y, neurons, 1, dist_threshold):

        update_neuron(image, neurons, neuron[0], neuron[1], lr * math.exp(- (neuron[2] * neuron[2]) / (neighbour_value * neighbour_value)))



def update_neuron(image, neurons, index_x, index_y, lr):
    a = neurons[index_x][index_y]
    sub = ne.evaluate('a - image')
    mult = ne.evaluate('sub*lr')
    neurons[index_x][index_y] = ne.evaluate('a - mult')
    #neurons[index_x][index_y] = np.subtract(neurons[index_x][index_y], np.multiply(np.subtract(neurons[index_x][index_y], image), lr))


'''
curr_neuron = int = index of current neuron
'''
def get_neighbouring_neurons(image, x, y, neurons, lr, dist_threshold):
    neighbours = []
    size = int(dist_threshold)
    cell = (x,y)
    for x in range(len(neurons)):
        for y in range(len(neurons[x])):
            dist = manhattan_distance(cell, (x,y))
            if(dist <= size):
                neighbours.append((x,y,dist))
    return neighbours


    # for c in product(*(range(n-1, n+2) for n in cell)):
    #     if c != cell and all(0 <= n < size for n in c):
    #         yield c


def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)

    # for x in range(len(neurons)):
    #     for y in range(len(neurons[x])):
    #         if(x == curr_neuron_x and y == curr_neuron_y):
    #             continue
    #         dist = euclideanDistance(neurons[x][y], neurons[curr_neuron_x][curr_neuron_y])
    #         if(dist <= dist_threshold):
    #             update_neuron(image, neurons, x, y, (1-translate(dist, 0, 199920, 0, 1))*0.1)


def assign_label(neurons, images, labels):
    assigned_neurons = {}
    for x in range(len(neurons)):
        for y in range(len(neurons[x])):
            current_best = (float('inf'), 0)
            for j in range(1000):
                random_image_index = random.randint(0, len(images)-1)
                image = images[random_image_index]
                label = labels[random_image_index]
                curr_dist = euclideanDistance(neurons[x][y], image)

                if(curr_dist < current_best[0]):
                    current_best = (curr_dist, random_image_index)
            if(x in assigned_neurons):
                assigned_neurons[x][y] = labels[current_best[1]]
            else:
                assigned_neurons[x] = {}
                assigned_neurons[x][y] = labels[current_best[1]]
    return assigned_neurons



    # assigned_neurons = []
    # for x in range(len(neurons)):
    #     for y in range(len(neurons[x])):
    #         current_best = (float('inf'), 0)
    #         for j in range(1000):
    #             random_image_index = random.randint(0, len(images)-1)
    #             image = images[random_image_index]
    #             label = labels[random_image_index]
    #             curr_dist = euclideanDistance(neurons[x][y], image)
    #
    #             if(curr_dist < current_best[0]):
    #                 current_best = (curr_dist, random_image_index)
    #         assigned_neurons.append(current_best[1])
    #
    # return assigned_neurons


def classify_image(neurons, labels, assignments, image):
    # votes = {}
    # for i in range(len(neurons)):
    #     curr_dist = euclideanDistance(neurons[i], image)
    #     if(labels[assignments[i][1]] in votes):
    #         votes[labels[assignments[i][1]]].append(curr_dist)
    #     else:
    #         votes[labels[assignments[i][1]]] = [curr_dist]
    # highest_voted_label = 0
    # vote = float('inf')
    # print('\n')
    # for key in votes:
    #     print(key, votes[key])
    #     curr_vote = np.average(votes[key])
    #     if(curr_vote < vote):
    #         vote = curr_vote
    #         highest_voted_label = key
    #
    # return (vote, highest_voted_label)

    current_best = (float('inf'), 0)
    for x in range(len(neurons)):
        for y in range(len(neurons[x])):
            curr_dist = euclideanDistance(neurons[x][y], image)
            if(curr_dist < current_best[0]):
                current_best = (curr_dist, x, y)

    return current_best


