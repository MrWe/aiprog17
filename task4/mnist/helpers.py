import numpy as np
def generate_neurons(num_neurons, num_weights):
    neurons = []
    for i in range(num_neurons):
        curr_weights = []
        for j in range(num_weights):
            curr_weights.append(np.random.uniform(-1,1))
        neurons.append(curr_weights)
    return neurons
