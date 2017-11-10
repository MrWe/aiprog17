import numpy as np
import random
def generate_neurons(num_neurons, num_weights):
    
    neurons = []
    for i in range(num_neurons):
        curr_weights = []
        for j in range(num_weights):
            curr_weights.append(np.random.uniform(0,1))
        neurons.append(curr_weights)
    return neurons

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
