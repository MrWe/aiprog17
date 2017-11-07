import random

def run(neurons, images, lr, lr_reduction_factor, num_neighbours, steps=1):

    for i in range(steps):
        random_image = random.choice(images)
        closest_neuron = shortest_dist(random_image, neurons)
        update_neurons(random_image, neurons, closest_neuron, lr, lr_reduction_factor, num_neighbours)
    return neurons


def euclideanDistance(neuron_weights, image_pixels):
    total = 0
    for i in range(len(neuron_weights)):
        total += pow(neuron_weights[i] - image_pixels[i], 2)
    return pow(total,0.5)


def shortest_dist(image_pixels, neuron_weights):
    sh = float("inf")
    index = 0
    for i in range(len(neuron_weights)):
        d = euclideanDistance(image_pixels, neuron_weights[i])
        if d < sh:
            sh = d
            index = i
    return index

def update_neurons(image, neurons, index, lr, lr_reduction_factor, num_neighbours):
    update_neuron(image, neurons, index, lr)

    # for x in range(num_neighbours):
    #     lr *= lr_reduction_factor
    #     update_neuron(image, neurons, (index+x) % len(neurons), lr)
    #     update_neuron(image, neurons, (index-x) % len(neurons), lr)


def update_neuron(image, neurons, index, lr):

    for i in range(len(neurons[index])):
        neurons[index][i] -= lr * (neurons[index][i] - image[i])




