#Params we need:
#File -> string
#learning rate -> float
#epochs(steps) -> int
#nbits=4
#lrate=0.03
#showint=300
#Minibatch size
#vfrac=0.1
#tfrac=0.1
#vint=100
#sm=False
#Number of layers
#Layer size
#Hidden activation function
#Output activation function -> default=softmax
#Cost function -> default=mean square error
#Initial wight range -> default=random(-0.5,0.5)
#Case fraction(fraction of dataset to be used) -> default=1.0
#Validation fraction(fraction of dataset to be used to validate)
#Test fraction(fraction of dataset to be used to test)
#Map batch size(The number of training cases to be used for a map test)
#Map layers(The layers to be visualized during the map test)
#Map dendrogram(List of the layers whose activation patterns (during map test) will be used to produce dendrogram, one per specified layer)
#Display weights(list of the wights to be visualized at the end of the run)
#Display biases(List of the biases to be visualized at the end of the run)
from GANN import *

#Input & output layer size should be set based on dataset and is therefore not listed.
def main():
    use_conf = False
    data_set = "glass"
    path = "data_sets/" + data_set + ".txt"
    epochs = 500
    lrate = 0.03
    showint = 300
    mbs = 10
    vfrac = 0.1
    tfrac = 0.1
    cfrac = 1.0
    vint = 1
    sm = False
    hidden_layers = [5,10,5]
    output_activation_function = 'softmax'
    cost_function = 'square'
    init_weight_range = [-.1, .1]
    init_bias_range = [-.1, .1]


    map_batch_size = 0.3 # number of cases to run mapping on
    # map_layers =
    # map_dendrogram =
    # display_weights =
    # display_biases =


    gradient_descent(dataset=path, epochs=epochs, nbits=hidden_layers, lrate=lrate, showint=showint, mbs=mbs,
    vfrac=vfrac, tfrac=tfrac, vint=vint, sm=sm, cfrac=cfrac, output_activation_function=output_activation_function,
    cost_function=cost_function, init_weight_range=init_weight_range, init_bias_range=init_bias_range)


if __name__ == '__main__':
    main()