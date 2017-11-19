#!/usr/bin/env python
import tkinter as tk
import tsp_som as tsp_som
import sys
from mnist.main import *
from mnist.helpers import *
from mnist.som import *
import read_file as rf
import math
import helper as hp
from itertools import groupby
from operator import itemgetter
import random
import time
import numpy as np
from time import gmtime, strftime
import pickle
import json



random.seed(123)

class App(tk.Frame):
  def __init__( self, parent):
    tk.Frame.__init__(self, parent)


    self.width = 800
    self.height = 800
    self.optimalTSP = [7542, 6110, 629, 22068, 14379, 108159, 59030, 1211]
    self.grid()
    self.checkboxValue = tk.IntVar()
    self.createWidgets()
    self._createCanvas()

  def start_mnist(self):

    self.pixel_size = 2


    print("Started mnist")

    #self.lr = 0.2
    self.epocs = 50
    self.neighbour_value = 10
    #ascii_neurons = main(self.num_neurons, self.num_weights)

    features = []
    labels = []
    for label, feature in read():
      labels.append(label)
      f = np.array(feature) / 255
      features.append(f.flatten().tolist())


    self.num_neurons = 450
    self.num_weights = len(features[0])
    self.row_length = len(f[0])

    neurons = generate_neurons(self.num_neurons, self.num_weights)

    self.width = len(neurons[0]) * len(f[0]) * self.pixel_size
    self._createCanvas()

    dist_threshold = 10;

    training_images = []

    s1 = time.time()



    for i in range(1,self.epocs):
      self.lr = np.exp(-i/16)
      root.update()
      neurons, images_this_turn = run(neurons, features, self.lr, 0.7, dist_threshold, self.neighbour_value, i, steps=100)
      dist_threshold = dist_threshold * dist_threshold**(-i/50)
      self.neighbour_value = self.neighbour_value * (1 - 0.01 * i)
      print("Epoch:", i)

      for j in range(len(images_this_turn)):
        training_images.append(images_this_turn[j])

      if(i % 10 == 0 and self.checkboxValue.get() == 1):

        print("Neighbour value:",self.neighbour_value)
        print("Learning rate:",self.lr)
        flat_neurons = [y for x in neurons for y in x]
        lined_neurons = []
        for p in range(len(flat_neurons)):
          lines = []
          for k in range(0,self.num_weights,self.row_length):
              lines.append(flat_neurons[p][k:k+self.row_length])
          lined_neurons.append(lines)
        self.show_mnist(lined_neurons, self.canvas)
    s2 = time.time()

    print("TIME: ", s2-s1)
    flat_neurons = [y for x in neurons for y in x]
    lined_neurons = []
    for p in range(len(flat_neurons)):
      lines = []
      for k in range(0,self.num_weights,self.row_length):
          lines.append(flat_neurons[p][k:k+self.row_length])
      lined_neurons.append(lines)
    self.show_mnist(lined_neurons, self.canvas)

    traning_rate, testing_rate = self.run_classification(None, training_images, neurons)
    self.fname = self.construct_filename([traning_rate, testing_rate])
    self.save_neurons_to_file(neurons, self.fname)


    print("FERDIG!")

  def construct_filename(self, args):
    fname = ""
    for i in range(len(args)):
      fname += str(args[i])
      if(i < len(args)-1):
        fname += "-"
    return fname

  def save_neurons_to_file(self, neurons, fname):
    path = "neurons/"
    output = open(path + str(fname), 'wb')
    pickle.dump(neurons, output)
    output.close()
    return fname

  def load_neurons_from_file(self, fname):
    path = "neurons/"
    pkl_file = open(path + fname, 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()
    return np.array(data)

  def run_classification(self, fname, training_images=None, n=None):



    if(fname == None):
      neurons = n
    else:
      neurons = self.load_neurons_from_file(fname)


    features = []
    labels = []
    for label, feature in read("training"):
      labels.append(label)
      f = np.array(feature) / 255
      features.append(f.flatten().tolist())
    assignments = assign_label(neurons, features, labels)


    #--------CLASSIFICATION-----------
    print("CLASSIFYING TRAINING SET")
    if(training_images == None):
      training_rate = self.classify(neurons, features, labels, assignments)
    else:
      training_rate = self.classify(neurons, features, labels, assignments, training_images)
    print("CLASSIFYING TESTING SET")

    features = []
    labels = []
    for label, feature in read("testing"):
      labels.append(label)
      f = np.array(feature) / 255
      features.append(f.flatten().tolist())

    testing_rate = self.classify(neurons, features, labels, assignments)

    return training_rate, testing_rate

  def classify(self, neurons, features, labels, assignments, indices=None):
    print("Starting classifications")


    num_correct_classifications = 0
    num_classifications = 0

    if(indices == None):
      random.seed(123)
      for j in range(100):
        root.update()
        random_image_index = random.randint(0, len(features)-1)
        image = features[random_image_index]
        label = labels[random_image_index]
        classification = classify_image(neurons, labels, assignments, image)
        classified_neuron = neurons[classification[1]][classification[2]]
        classification_value = assignments[classification[1]][classification[2]]

        if(classification_value == label):
          num_correct_classifications += 1
        if(j % 100 == 0 and self.checkboxValue.get() == 1):
          classifications = []

          lined_neuron = []
          for k in range(0,self.num_weights,self.row_length):
              lined_neuron.append(classified_neuron[k:k+self.row_length])
          classifications.append(lined_neuron)

          lined_image = []
          for k in range(0,self.num_weights,self.row_length):
              lined_image.append(image[k:k+self.row_length])
          classifications.append(lined_image)
          self.show_mnist(classifications, self.canvas2, label1=label, label2=classification_value)
      print("Number of correct:", num_correct_classifications )
      print("Total number of classifications:", j)
      if(j > 0):
        print("Success rate:", num_correct_classifications / j)
      return round(num_correct_classifications / j, 2)

    else:
      print("Number of classification cases:", len(indices))
      for j in range(len(indices)):
        root.update()
        num_classifications += 1
        image_index = indices[j]
        image = features[image_index]
        label = labels[image_index]
        classification = classify_image(neurons, labels, assignments, image)
        classified_neuron = neurons[classification[1]][classification[2]]
        classification_value = assignments[classification[1]][classification[2]]

        if(classification_value == label):
          num_correct_classifications += 1
        if(j % 100 == 0 and self.checkboxValue.get() == 1):
          classifications = []

          lined_neuron = []
          for k in range(0,self.num_weights,self.row_length):
              lined_neuron.append(classified_neuron[k:k+self.row_length])
          classifications.append(lined_neuron)

          lined_image = []
          for k in range(0,self.num_weights,self.row_length):
              lined_image.append(image[k:k+self.row_length])
          classifications.append(lined_image)
          self.show_mnist(classifications, self.canvas2, label1=label, label2=classification_value)
      print("Number of correct:", num_correct_classifications )
      print("Total number of classifications:", j)
      if(j > 0):
        print("Success rate:", num_correct_classifications / num_classifications)
      return round(num_correct_classifications / num_classifications, 2)



  def sort_neurons(self, neurons):

    sorted_array = []
    sorted_array.append(neurons[0])

    for i in range(1, len(neurons)-2):
        inserted = False
        for j in range(i+2, len(neurons)):
          if euclideanDistance(neurons[i], neurons[i+1]) > euclideanDistance(neurons[i], neurons[j]):
            best = neurons[j]
            worst = neurons[i+1]
            neurons[i+1] = best
            neurons[j] = worst

        #     sorted_array.insert(j, neurons[i])
        #     inserted = True
        #     break
        # if(not inserted):
        #   sorted_array.append(neurons[i])
    return neurons


  def show_mnist(self, neurons, canvas, size=2, label1=None, label2=None):
    canvas.delete("all")

    offset_x = 0
    offset_y = 0

    for k in range(len(neurons)): #[[[0.12314, 0,1234...],[0.1552, 0.901823],[...],...]] k er hver rad
      x = 0
      y = 0
      for l in range(len(neurons[k])): #[[0.123125, 0.59238, ...],[0.123129, 0.948594, ...], ...] l er hvert nevron
        x = 0
        for j in range(len(neurons[k][l])): #[0.1239123, 0.2348934, ...] j er hver vekt

          coords = (x+offset_x,y + offset_y,offset_x+x+size,offset_y+y+size)
          x += size

          curr_fill = (int(neurons[k][l][j] * 255), int(neurons[k][l][j] * 255), int(neurons[k][l][j] * 255))
          fill = '#%02x%02x%02x' % curr_fill

          canvas.create_rectangle(coords, outline="", fill=fill, width=1, state='disabled')
          # canvas.create_text(x+offset_x, y + offset_y+50, text=(label1, label2))
        y += size
      offset_x += size * 28
      if(offset_x + size * 28 >= self.width + 30):
        offset_y += size * 28
        offset_x = 0


  def start_tsp(self):
    self.init_neuron_radius, self.learning_rate, self.learning_rate_decay, self.lr_reduction_factor, self.epochs, self.neurons_multiplier, self.num_neighbours, self.steps = self.read_config()
    self.self_org_map = tsp_som
    self.cities, self.none_scaled_cities, self.max_x, self.min_x, self.max_y, self.min_y = rf.read_file('data/'+ self.entry.get() + '.txt', self.width, self.height)
    if(self.entry.get() == "8"):
      self.cities = self.none_scaled_cities
    self.neurons = self.init_neurons()

    self.draw_points(self.cities)
    self.on_start_press()

  def read_config(self):
      board = self.entry.get()
      try:
        with open('config.json') as f:
            d = json.load(f)
        config = d[board]
      except:
        print("Using fallback parameters")
        config = {
        "learning_rate": 0.1,
        "learning_rate_decay": 20,
        "init_neuron_radius": 50,
        "learning_rate": 1.1,
        "lr_reduction_factor": 0.7,
        "epochs": 100,
        "neurons_multiplier": 3,
        "num_neighbours": 100,
        "steps": 20
        }
      return config['init_neuron_radius'], config['learning_rate'], config['learning_rate_decay'], config['lr_reduction_factor'], config['epochs'], config['neurons_multiplier'], config['num_neighbours'], config['steps']

  #NOTE: gui is locked until this is finished
  def on_start_press(self):
    for i in range(self.epochs):
      self.neurons = self.self_org_map.run(self.neurons, self.cities, np.exp(-i/self.learning_rate_decay), self.lr_reduction_factor, self.num_neighbours, self.steps)
      root.update()
      if(self.checkboxValue.get() == 1):
        self.show_board(self.neurons)
      self.learning_rate *= 0.999
      if(i%100 == 0):
        self.num_neighbours -= 1
    self.ordered_cities = self.self_org_map.calculate_finished_path(self.neurons, self.cities)
    self.ordered_cities = self.self_org_map.enhance_finished_path(self.ordered_cities)
    self.show_board(self.ordered_cities)

    if(self.entry.get() is not "8"):
      self.re_mapped_cities = []
      for i in range(len(self.ordered_cities)):
        x = hp.translate(self.ordered_cities[i][0], 10, self.width-10, self.min_x, self.max_x)
        y = hp.translate(self.ordered_cities[i][1], 10, self.height-10, self.min_y, self.max_y)
        self.re_mapped_cities.append([x,y])
      self.re_mapped_cities = self.self_org_map.enhance_finished_path(self.re_mapped_cities)

    if(self.entry.get() == "8"):
      path_length = self.self_org_map.get_path_length(self.ordered_cities)
    else:
      path_length = self.self_org_map.get_path_length(self.re_mapped_cities)
    optimal_path_length = self.optimalTSP[int(self.entry.get())-1]
    print("Board: ", self.entry.get())
    print("Path length:", path_length)
    print("Optimal length:", optimal_path_length)
    print("percent above optimal:", ((path_length / optimal_path_length)*100)-100)
    print("\n")



  def init_neurons(self):
    num_neurons = int(len(self.cities) * self.neurons_multiplier)
    centerx,centery = self.self_org_map.centeroidnp(np.array(self.cities))
    neurons = []
    for i in range(num_neurons):
      circ_x = centerx + self.init_neuron_radius * math.cos(hp.translate(i, 0, num_neurons, 0, math.pi*2))
      circ_y = centery + self.init_neuron_radius * math.sin(hp.translate(i, 0, num_neurons, 0, math.pi*2))
      neurons.append([circ_x, circ_y])
    return neurons

  def createWidgets(self):
    self.startButton = tk.Button(text="Start TSP", command=lambda : self.start_tsp())
    self.startButton.grid()

    self.mnistButton = tk.Button(text="Start MNIST", command=lambda : self.start_mnist())
    self.mnistButton.grid()

    self.exitButton = tk.Button(text="Exit", command=lambda : exit())
    self.exitButton.grid()

    self.entryClas = tk.Entry()
    self.entryClas.pack()
    self.entryClas.insert(0,'Classification')
    self.entryClas.grid(row=1, column=1)

    self.classificationButton = tk.Button(text="Run only classification", command=lambda : self.run_classification(self.entryClas.get()))
    self.classificationButton.grid(row=2, column=1)


    self.entry = tk.Entry()
    self.entry.pack()
    self.entry.insert(0,'1')
    self.entry.grid()

    self.visualizeCheckbutton = tk.Checkbutton(text="Enable visualization", variable=self.checkboxValue)
    self.visualizeCheckbutton.grid()

  def _createCanvas(self):
    self.canvas = tk.Canvas(width = self.width, height = self.height,
                            bg = "grey" )
    self.canvas.grid(row=0, column=0, sticky='nsew')
    self.canvas2 = tk.Canvas(width = self.width, height = self.height,
                            bg = "grey" )
    self.canvas2.grid(row=0, column=1, sticky='nsew')

  def show_board(self, points):
    self.canvas.delete("all")
    self.draw_polygon(points)
    self.draw_points(self.cities)


  def draw_points(self, points, fill='#ff0000'):
    for i in range(len(points)):
      coords = (points[i][0],points[i][1],points[i][0]+3,points[i][1]+3)
      self.canvas.create_rectangle(coords, fill=fill, width=1, state='disabled')

  def draw_polygon(self,points):
    self.canvas.create_polygon(points, outline='#000000', fill='', width=1, state='disabled')
    self.draw_points(self.neurons,'#0000ff')


if __name__ == "__main__":
  root = tk.Tk()
  root.geometry( "1500x1000" )
  app = App(root)
  root.mainloop()
