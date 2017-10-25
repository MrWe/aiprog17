from GANN import *
from casemanager import *
from load_dataset import load_data, get_valid_mnist
import tflowtools as TFT
import json
<<<<<<< Updated upstream
import random

random.seed(123)
np.random.seed(123)
tf.set_random_seed(123)
=======
import sys
import mnist_basics as mnist
>>>>>>> Stashed changes

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
        map_layers = data["map_layers"]
        map_grabvars = data["map_grabvars"]
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
        layers=[size]
        layers.extend(hidden_layers)
        layers.append(size)
    elif(data_set == "parity"):
        size = 2**nbits
        mbs = mbs if mbs else size
        case_generator = (lambda : TFT.gen_all_parity_cases(size))
        cman = Caseman(cfunc=case_generator,vfrac=vfrac,tfrac=tfrac)
        layers=[size]
        layers.extend(hidden_layers)
        layers.append(2)
    elif(data_set == "bit_counter"):
        size = 2**nbits
        mbs = mbs if mbs else size
        case_generator = (lambda : TFT.gen_vector_count_cases(2**size,size))
        cman = Caseman(cfunc=case_generator,vfrac=vfrac,tfrac=tfrac)
        layers=[size]
        layers.extend(hidden_layers)
        layers.append(size+1)
    elif(data_set == "mnist"):
        data = get_valid_mnist()

        size_in = len(data[0][0])
        size_out = len(data[0][1])

        layers = [size_in]

        layers.extend(hidden_layers)
        layers.append(size_out)

        mbs = mbs if mbs else size
        case_generator = (lambda : get_valid_mnist())
        cman = Caseman(cfunc=case_generator,vfrac=vfrac,tfrac=tfrac)

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
    hidden_activation_function=hidden_activation_function,cost_function=cost_function, init_weight_range=init_weight_range,
    init_bias_range=init_bias_range, map_batch_size=map_batch_size,show_layers=show_layers, grabvars=grabvars,
    map_layers=map_layers,map_grabvars=map_grabvars)





if __name__ == '__main__':

    main()
    while(True):
        if(input("ENTER to exit") != ""):
            main()
        else:
            break
