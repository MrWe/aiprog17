import networkx as nx
import numpy as np
#import helpers as hp
#import mnist_reader as mr
#import som
from mnist.helpers import *
from mnist.som import *
from mnist.mnist_reader import *



def main(num_neurons=50, num_weights=784):
    neurons = generate_neurons(num_neurons, num_weights)
    features = []
    labels = []
    for label, feature in read():
        labels.append(label)
        f = np.array(feature) / 255
        features.append(f.flatten().tolist())

    dist_threshold = 199920;



    for i in range(5000):
        neurons = run(neurons, features, 0.01, 0.9, dist_threshold, steps=1)
        dist_threshold *= 0.7


    lol = []
    for p in range(len(neurons)):
        for j in range(len(neurons[0])):
            if(neurons[p][j] < 0.3):
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



#if __name__ == '__main__':
#    main()