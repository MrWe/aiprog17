import random
import numpy as np
import numexpr as ne
import itertools as it
random.seed(123)

def run(neurons, cities, lr, lr_reduction_factor, num_neighbours, steps=10):

    random.seed(123)
    random.shuffle(cities)
    for i in range(len(cities)):
        #random_city = random.choice(cities)
        closest_neuron = shortest_dist(cities[i], neurons)
        update_neurons(cities[i], neurons, closest_neuron, lr, lr_reduction_factor, num_neighbours)
    return neurons


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
    neurons[index][0] -= dir_x
    neurons[index][1] -= dir_y

def get_path_length(neurons):
    length = 0
    for i in range(len(neurons)):
        if(i == len(neurons)-1):
            length += euclideanDistance(neurons[i], neurons[0])
        else:
            length += euclideanDistance(neurons[i], neurons[i+1])
    return length

#hp.translate(self.ordered_cities[i][1], 10, self.height-10, self.min_y, self.max_y)

def calculate_finished_path(neurons, cities):
    closest_neurons = {}
    cities_order = []
    for i in range(len(cities)):
        shortest = shortest_dist(cities[i], neurons)
        if(shortest in closest_neurons):
            closest_neurons[shortest].append(cities[i])
        else:
            closest_neurons[shortest] = [cities[i]]

    for i in range(len(neurons)):
        if(i in closest_neurons):
            for j in range(len(closest_neurons[i])):
                cities_order.append(closest_neurons[i][j])
    return cities_order


def enhance_finished_path(cities):
    dist_to_shuffle = 5
    best_path_length = get_path_length(cities)
    best_path_cities = cities
    should_run_again = True
    while(should_run_again):
        should_run_again = False
        for i in range(len(best_path_cities)):
            part = best_path_cities[i:i+dist_to_shuffle]
            first = best_path_cities[:i]
            last = best_path_cities[i+dist_to_shuffle:]
            all_perms = list(it.permutations(part))
            for j in range(len(all_perms)):
                test_path = first + list(all_perms[j]) + last
                curr_path_length = get_path_length(test_path)
                if(curr_path_length < best_path_length):
                    best_path_length = curr_path_length
                    best_path_cities = test_path
                    should_run_again = True
    best_path_cities_copy = best_path_cities[:]
    dist_to_shuffle = 2
    should_run_again = True
    while(should_run_again):
        should_run_again = False
        for i in range(len(best_path_cities)):
            part = best_path_cities[i-dist_to_shuffle:i+dist_to_shuffle]
            first = best_path_cities[:i-dist_to_shuffle]
            last = best_path_cities[i+dist_to_shuffle:]
            all_perms = list(it.permutations(part))
            for j in range(len(all_perms)):
                test_path = first + list(all_perms[j]) + last
                curr_path_length = get_path_length(test_path)
                if(curr_path_length < best_path_length):

                    best_path_length = curr_path_length
                    best_path_cities = test_path
                    should_run_again = True


    return best_path_cities




def centeroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length



