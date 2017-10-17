import os
import numpy as np
import tflowtools as TFT
import tensorflow as tf
import fileinput
import random


def replaceSeparator(file):
    with open(file, "r") as file:
        with open("data_sets/gamma.txt.bak", "w") as out:
            for line in file:
                if(random.uniform(0, 1) > 0.5):
                    out.write(line)


def max_label(file):
    #replaceSeparator(file)

    f = open(file)
    separator = ','
    lines = []
    max_length = 0
    for line in f.readlines():
        label = int(line.split(separator)[-1].strip())
        if(max_length < label):
            max_length = label

    f.close()
    return max_length

def load_data(file, cfrac):
    one_hot_length = max_label(file);
    f = open(file)
    separator = ','
    lines = []

    for line in f.readlines():
        if(random.random() <= cfrac):
            feature = line.split(separator)[:-1]
            label = TFT.int_to_one_hot(int(line.split(separator)[-1].strip())-1, one_hot_length)
            lines.append(np.array([feature, label]))
    return lines

def quickrun(operators, grabbed_vars=None, dir='probeview', session=None, feed_dict=None, step=1, show_interval=1):
    sess = session if session else TFT.gen_initialized_session(dir=dir)

    results = sess.run([operators, grabbed_vars], feed_dict=feed_dict)
    if show_interval and (step % show_interval) == 0:
        TFT.show_results(results[1], grabbed_vars, dir)
    return results[0], results[1], sess

def gradient_descent(filename, size_features=9, steps=1000, tvect=None, learning_rate=0.5, showint=10):
    features, labels = load_data(filename)
    #features = np.array([features[0]])
    print("X SHAPE", features.shape)

    target = tvect if tvect else np.array(labels[0]) # We have 7 different possible outputs

    w = tf.Variable(np.random.uniform(-0.1, 0.1, size=(size_features, size_features)), name='weights') # We will train these #None = 214
    print("W SHAPE:", w.shape)
    b = tf.Variable(np.zeros((1, size_features)), name='bias')

    x = tf.placeholder(tf.float64, shape=(214, size_features), name='input')
    print("X SHAPE:", x.shape)
    y = tf.tanh(tf.matmul(x, w) + b, name='out-softplus')

    error = tf.reduce_mean(tf.square(target - y))

    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    training_operator = optimizer.minimize(error)

    feeder = {x: features} #this is our data

    sess = TFT.gen_initialized_session()
    for step in range(steps):

        quickrun([training_operator], [w, b, y, error], session=sess, feed_dict=feeder, step=step, show_interval=showint)
    TFT.close_session(sess)

#print(gradient_descent('data_sets/glass.txt'))