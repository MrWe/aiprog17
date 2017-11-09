import math
import random
import numpy as np
#import helpers as hp
from mnist.helpers import *

random.seed(123)

def run(neurons, images, lr, lr_reduction_factor, dist_threshold, steps=1):
    random.seed(123)
    for i in range(steps):
        random_image = random.choice(images)
        closest_neuron = shortest_dist(random_image, neurons)
        update_neurons(random_image, neurons, closest_neuron, lr, lr_reduction_factor, dist_threshold)
    return neurons


def euclideanDistance(neuron_weights, image_pixels):
    # total = 0
    # for i in range(len(neuron_weights)):
    #     total += pow(neuron_weights[i] - image_pixels[i], 2)
    # return pow(total,0.5)
    return np.sqrt(np.sum(np.power(np.subtract(neuron_weights, image_pixels),2)))


def shortest_dist(image_pixels, neuron_weights):
    sh = float("inf")
    index = 0
    for i in range(len(neuron_weights)):
        d = euclideanDistance(image_pixels, neuron_weights[i])
        if d < sh:
            sh = d
            index = i
    return index

def update_neurons(image, neurons, index, lr, lr_reduction_factor, dist_threshold):
    update_neuron(image, neurons, index, lr)
    update_neighbouring_neurons(image, index, neurons, 1, dist_threshold)


def update_neuron(image, neurons, index, lr):
    # neurons[index] = np.subtract(neurons[index],np.subtract(neurons[index], np.multiply(image, lr)))
    # neurons[index] = neurons[index].tolist()
    for i in range(len(neurons[index])):
        neurons[index][i] -= (lr * (neurons[index][i] - image[i]))


'''
curr_neuron = int = index of current neuron
'''
def update_neighbouring_neurons(image, curr_neuron, neurons, lr, dist_threshold):
    for i in range(len(neurons)):
        if(i == curr_neuron):
            continue
        dist = euclideanDistance(neurons[i], neurons[curr_neuron])
        if(dist <= dist_threshold):
            update_neuron(image, neurons, i, (1-translate(dist, 0, 199920, 0, 1))*0.05)


def assign_label(neurons, images, labels):
    random.seed(123)
    assigned_neurons = []
    for i in range(len(neurons)):
        current_best = (float('inf'), 0)
        for j in range(1000):
            random_image_index = random.randint(0, len(images)-1)
            image = images[random_image_index]
            label = labels[random_image_index]
            curr_dist = euclideanDistance(neurons[i], image)
            if(curr_dist < current_best[0]):
                current_best = (curr_dist, random_image_index)
        assigned_neurons.append(current_best)

    return assigned_neurons


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
    for i in range(len(neurons)):
        curr_dist = euclideanDistance(neurons[i], image)
        if(curr_dist < current_best[0]):
            current_best = (curr_dist, i)

    return current_best


