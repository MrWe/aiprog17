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



class App(tk.Frame):
  def __init__( self, parent):
    tk.Frame.__init__(self, parent)


    self.width = 700
    self.height = 800
    self.grid()
    self.checkboxValue = tk.IntVar()
    self.createWidgets()
    self._createCanvas()

  def start_tsp(self):
    self.init_neuron_radius = 50
    self.learning_rate = 1.1
    self.lr_reduction_factor = 0.6
    self.epochs = 2000
    self.neurons_multiplier = 3
    self.num_neighbours = 50
    self.steps = 20
    self.path_length = 0
    self.self_org_map = tsp_som
    self.cities, self.max_x, self.min_x, self.max_y, self.min_y = rf.read_file('data/'+ self.entry.get() + '.txt', self.width, self.height)
    self.neurons = self.init_neurons()

    self.draw_points(self.cities)
    self.on_start_press()

  def start_mnist(self):


    print("Started mnist")

    self.lr = 0.5
    #ascii_neurons = main(self.num_neurons, self.num_weights)


    features = []
    labels = []
    for label, feature in read():
      labels.append(label)
      f = np.array(feature) / 255
      features.append(f.flatten().tolist())

    self.num_neurons = 100
    self.num_weights = len(features[0])

    neurons = generate_neurons(self.num_neurons, self.num_weights)

    dist_threshold = 199920;

    for i in range(3000):
      root.update()
      neurons = run(neurons, features, self.lr, 0.7, dist_threshold, steps=1)
      dist_threshold = dist_threshold * dist_threshold**(-i/30000)

      if(i % 100 == 0 and self.checkboxValue.get() == 1):
        neurons = self.sort_neurons(neurons)

        ascii_neurons = []
        for p in range(len(neurons)):
          ascii_neuron = []
          for k in range(0,784,28):
              ascii_neuron.append(neurons[p][k:k+28])
          ascii_neurons.append(ascii_neuron)
        self.show_mnist(ascii_neurons, self.canvas)
    # for i in range(len(neurons)):
    #   for k in range(len(neurons[i])):
    #     for l in range(len(neurons[i])):
    #       if(neurons[i][l] < 0.2):
    #         neurons[i][l] = 0.0
    # ascii_neurons = []
    # for p in range(len(neurons)):
    #   ascii_neuron = []
    #   for k in range(0,784,28):
    #       ascii_neuron.append(neurons[p][k:k+28])
    #   ascii_neurons.append(ascii_neuron)
    # self.show_mnist(ascii_neurons, self.canvas)
    assignments = assign_label(neurons, features, labels)



    num_correct_classifications = 0

    for j in range(1000):
      root.update()
      random_image_index = random.randint(0, len(features)-1)
      image = features[random_image_index]
      label = labels[random_image_index]
      if(j % 10 == 0 and self.checkboxValue.get() == 1):
        ascii_neurons = []
        for p in range(len([image])):
          ascii_neuron = []
          for k in range(0,784,28):
              ascii_neuron.append([image][p][k:k+28])
          ascii_neurons.append(ascii_neuron)
        for p in range(len([neurons[classify_image(neurons, labels, assignments, image)[1]]])):
          ascii_neuron = []
          for k in range(0,784,28):
              ascii_neuron.append([neurons[classify_image(neurons, labels, assignments, image)[1]]][p][k:k+28])
          ascii_neurons.append(ascii_neuron)
        self.show_mnist(ascii_neurons, self.canvas2)
      if(labels[assignments[classify_image(neurons, labels, assignments, image)[1]][1]] == label):
        num_correct_classifications += 1
    print("Number of correct:", num_correct_classifications )
    print("Total number of classifications:", j)
    if(j > 0):
      print("Error rate:", num_correct_classifications / j)
      # print("Label: ", label)
      # print("Guess: ", labels[assignments[classify_image(neurons, image)[1]][1]])
      #print((label,assignments[classify_image(neurons, image)[1]][1]))


    # for l in range(10):
    #   print(labels[assignments[l][1]])
    print("FERDIG!")


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


  def show_mnist(self, neurons, canvas, size=2):
    canvas.delete("all")

    size = size
    offset_x = 0
    offset_y = 0

    for k in range(len(neurons)):
      x = 0
      y = 0
      for i in range(len(neurons[k])):
        x = 0
        for j in range(len(neurons[k][i])):
          coords = (x+offset_x,y + offset_y,offset_x+x+size,offset_y+y+size)
          x += size
          curr_fill = (int(neurons[k][i][j] * 255), int(neurons[k][i][j] * 255), int(neurons[k][i][j] * 255))
          fill = '#%02x%02x%02x' % curr_fill
          canvas.create_rectangle(coords, outline="", fill=fill, width=1, state='disabled')
        y += size
      offset_x += size * 28
      if(offset_x + size * 28 >= self.width+10):
        offset_y += size * 28
        offset_x = 0


  #NOTE: gui is locked until this is finished
  def on_start_press(self):
    for i in range(self.epochs):
      self.neurons, self.path_length = self.self_org_map.run(self.neurons, self.cities, self.learning_rate, self.lr_reduction_factor, self.num_neighbours, self.steps)
      root.update()
      if(self.checkboxValue.get() == 1):
        self.show_board(self.neurons)
      self.learning_rate *= 0.999
      if(i%100 == 0):
        self.num_neighbours -= 1
    self.re_mapped_neurons = []
    for i in range(len(self.neurons)):
      x = hp.translate(self.neurons[i][0], 10, self.width-10, self.min_x, self.max_x)
      y = hp.translate(self.neurons[i][1], 10, self.height-10, self.min_y, self.max_y)
      self.re_mapped_neurons.append([x,y])
    print(self.self_org_map.get_path_length(self.re_mapped_neurons))


  def init_neurons(self):
    num_neurons = len(self.cities) * self.neurons_multiplier
    neurons = []
    for i in range(num_neurons):
      circ_x = self.width/2 + self.init_neuron_radius * math.cos(hp.translate(i, 0, num_neurons, 0, math.pi*2))
      circ_y = self.height/2 + self.init_neuron_radius * math.sin(hp.translate(i, 0, num_neurons, 0, math.pi*2))
      neurons.append([circ_x, circ_y])
    return neurons

  def createWidgets(self):
    self.startButton = tk.Button(text="Start TSP", command=lambda : self.start_tsp())
    self.startButton.grid()

    self.mnistButton = tk.Button(text="Start MNIST", command=lambda : self.start_mnist())
    self.mnistButton.grid()

    self.exitButton = tk.Button(text="Exit", command=lambda : exit())
    self.exitButton.grid()

    self.entry = tk.Entry()
    self.entry.pack()
    self.entry.insert(0,'1')
    self.entry.grid()

    self.visualizeCheckbutton = tk.Checkbutton(text="Enable visualations", variable=self.checkboxValue)
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
