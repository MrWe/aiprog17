import random

def run(neurons, cities, lr, lr_reduction_factor, num_neighbours, steps=10):
    for i in range(steps):
        random_city = random.choice(cities)
        closest_neuron = shortest_dist(random_city, neurons)
        update_neurons(random_city, neurons, closest_neuron, lr, lr_reduction_factor, num_neighbours)
    return neurons, get_path_length(neurons)


def euclideanDistance(coordinate1, coordinate2):
    return pow(pow(coordinate1[0] - coordinate2[0], 2) + pow(coordinate1[1] - coordinate2[1], 2), .5)


def shortest_dist(city, neurons):
    sh = float("inf")
    index = 0
    for i in range(len(neurons)):
        d = euclideanDistance(city, neurons[i])
        if d < sh:
            sh = d
            index = i
    return index

def update_neurons(city, neurons, index, lr, lr_reduction_factor, num_neighbours):
    update_neuron(city, neurons, index, lr)

    for x in range(num_neighbours):
        lr *= lr_reduction_factor
        update_neuron(city, neurons, (index+x) % len(neurons), lr)
        update_neuron(city, neurons, (index-x) % len(neurons), lr)


def update_neuron(city, neurons, index, lr):
    dir_x = lr * (neurons[index][0] - city[0])
    dir_y = lr * (neurons[index][1] - city[1])
    neurons[index][0] -= dir_x*lr
    neurons[index][1] -= dir_y*lr

def get_path_length(neurons):
    length = 0
    for i in range(len(neurons)):
        if(i == len(neurons)-1):
            length += euclideanDistance(neurons[i], neurons[0])
        else:
            length += euclideanDistance(neurons[i], neurons[i+1])
    return length



