#import networkx as nx
import numpy as np
import helpers as hp
import mnist_reader as mr
import som



def main(num_neurons=1, num_weights=784):
    neurons = hp.generate_neurons(num_neurons, num_weights)
    features = []
    labels = []
    for label, feature in mr.read():
        labels.append(label)
        f = np.array(feature) / 255
        features.append(f.flatten().tolist())
    print(neurons[0])
    for i in range(100):
        neurons = som.run(neurons, features, 0.01, 1, 1, steps=10)
    print(neurons[0])


if __name__ == '__main__':
    main()