#import networkx as nx
import numpy as np
import helpers as hp
import mnist_reader as mr
import som



def main(num_neurons=10, num_weights=784):
    neurons = hp.generate_neurons(num_neurons, num_weights)
    features = []
    labels = []
    for label, feature in mr.read():
        labels.append(label)
        f = np.array(feature) / 255
        features.append(f.flatten().tolist())



    for i in range(5000):

        neurons, update_index = som.run(neurons, features, 0.0001, 0.9999, 1, steps=1)

    lol = []
    for p in range(len(neurons)):
        for j in range(len(neurons[0])):
            if(neurons[p][j] < 0.01):
                neurons[p][j] = '0'
            else:
                neurons[p][j] = '-'
        lol2 = []
        for k in range(0,784,28):
            lol2.append(neurons[p][k:k+28])
        lol.append(lol2)

    for l in lol:
        for h in l:
            print(h)
        print('\n')



if __name__ == '__main__':
    main()