import os
import numpy as np
import tflowtools as TFT
import tensorflow as tf

def load_data(file):
    f = open(file)

    features = []
    labels = []
    for line in f.readlines():
        features.append(line.split(',')[:-1])
        labels.append(line.split(',')[-1].strip())

    return np.array(features), np.array(labels)

def quickrun(operators, grabbed_vars=None, dir='probeview', session=None, feed_dict=None, step=1, show_interval=1):
    sess = session if session else TFT.gen_initialized_session(dir=dir)

    results = sess.run([operators, grabbed_vars], feed_dict=feed_dict)
    if show_interval and (step % show_interval) == 0:
        TFT.show_results(results[1], grabbed_vars, dir)
    return results[0], results[1], sess

def gradient_descent(filename, size_features=9, size_labels=7, steps=50, tvect=None, learning_rate=0.5, showint=10):
    features, labels = load_data(filename)
    print("X SHAPE")
    print(features.shape)
    target = tvect if tvect else labels # We have 7 different possible outputs

    w = tf.Variable(np.random.uniform(-0.1, 0.1, size=(214, 214)), name='weights') # We will train these #None = 214
    print("W SHAPE:", w.shape)
    b = tf.Variable(np.zeros((1, 214)), name='bias')

    x = tf.placeholder(tf.float64, shape=(214, 214), name='input')
    print("X SHAPE:", x.shape)
    y = tf.sigmoid(tf.matmul(w, x) + b, name='out-sigmoid')

    error = tf.reduce_mean(tf.square(target - y))

    optimizer = tf.train.GradientDescentOptimizer(learning_rate) #ikke tenk
    training_operator = optimizer.minimize(error)

    feeder = {x: features} #this is our data lol

    sess = TFT.gen_initialized_session()
    for step in range(steps):
        quickrun([training_operator], [w, b, y], session=sess, feed_dict=feeder, step=step, show_interval=showint)
    TFT.close_session(sess)

print(gradient_descent('data_sets/glass.txt'))