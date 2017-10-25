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
from casemanager import *
from load_dataset import load_data
import tflowtools as TFT
import json

file_sets = ["wine", "glass", "gamma", "yeast"];

#Input & output layer size should be set based on dataset and is therefore not listed.
def main():
    data_set = ""
    with open("conf.json") as jfile:
        data = json.load(jfile)
        data_set = data["data_set"]
        map_batch_size = data["map_batch_size"]
        show_layers = data["show_layers"]
        grabvars = data["grabvars"]
        epochs = data[data_set]["epochs"]
        lrate = data[data_set]["lrate"]
        showint = data[data_set]["showint"]
        mbs = data[data_set]["mbs"]
        vfrac = data[data_set]["vfrac"]
        tfrac = data[data_set]["tfrac"]
        cfrac = data[data_set]["cfrac"]
        vint = data[data_set]["vint"]
        hidden_layers = data[data_set]["hidden_layers"]
        output_activation_function = data[data_set]["output_activation_function"]
        hidden_activation_function = data[data_set]["hidden_activation_function"]
        cost_function = data[data_set]["cost_function"]
        init_weight_range = data[data_set]["init_weight_range"]
        init_bias_range = data[data_set]["init_bias_range"]
        if(data_set not in file_sets):
            nbits = data[data_set]["nbits"]
        else:
            path = "data_sets/"+data_set+".txt"


    if(data_set == "autoEncode"):
        size = 2**nbits
        mbs = mbs if mbs else size
        case_generator = (lambda : TFT.gen_all_one_hot_cases(2**nbits))
        cman = Caseman(cfunc=case_generator,vfrac=vfrac,tfrac=tfrac)
        layers=[size,nbits,size]
    elif(data_set == "parity"):
        size = 2**nbits
        mbs = mbs if mbs else size
        case_generator = (lambda : TFT.gen_all_parity_cases(size))
        cman = Caseman(cfunc=case_generator,vfrac=vfrac,tfrac=tfrac)
        layers=[size]
        layers.extend(hidden_layers)
        layers.append(2)
    else:
        data = load_data(path, cfrac)

        size_in = len(data[0][0])
        size_out = len(data[0][1])

        layers = [size_in]

        layers.extend(hidden_layers)
        layers.append(size_out)

        mbs = mbs if mbs else size
        case_generator = (lambda : load_data(path, cfrac))
        cman = Caseman(cfunc=case_generator,vfrac=vfrac,tfrac=tfrac)

    #map_layers =
    # map_dendrogram =
    # display_weights =
    # display_biases =


    gradient_descent(epochs=epochs, dims=layers, cman=cman, lrate=lrate, showint=showint, mbs=mbs,
    vfrac=vfrac, tfrac=tfrac, vint=vint, cfrac=cfrac, output_activation_function=output_activation_function,
    hidden_activation_function=hidden_activation_function,cost_function=cost_function, init_weight_range=init_weight_range, init_bias_range=init_bias_range, map_batch_size=map_batch_size,show_layers=show_layers, grabvars=grabvars)


if __name__ == '__main__':
    main()
    while(True):
        if(input("ENTER to exit") != ""):
            main()
        else:
            break
