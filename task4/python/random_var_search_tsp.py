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


class App():
  def __init__(self):
    self.optimalTSP = [7542, 6110, 629, 22068, 14379, 108159, 59030, 1211]
    self.board = 1
    count = 0
    self.self_org_map = tsp_som


    while(True):

      self.optimal_count = 0
      self.init_neuron_radius = random.randint(0, 1000)
      self.learning_rate = random.uniform(0.001, 10)
      self.learning_rate_decay = random.uniform(0.00001, 10)
      self.lr_reduction_factor = random.uniform(0.00001, 1)
      self.epochs = random.randint(1, 100)
      self.neurons_multiplier = random.randint(1, 10)
      self.num_neighbours = random.randint(1, 1000)
      self.steps = random.randint(1, 100)

      for i in range(1, 9):
        self.board = i
        self.cities, self.max_x, self.min_x, self.max_y, self.min_y = rf.read_file('data/'+ str(i) + '.txt', 800, 800)
        self.neurons = self.init_neurons()
        should_break = self.on_start_press()
        if(self.optimal_count > 5):
          print("Number of correct: ", self.optimal_count)
          print('''
            "learning_rate":''' +  str(self.learning_rate) + ''',
            "learning_rate_decay":''' + str(self.learning_rate_decay) + ''',
            "init_neuron_radius":''' + str(self.init_neuron_radius) + ''',
            "lr_reduction_factor":'''+ str(self.lr_reduction_factor)+''',
            "epochs": '''+str(self.epochs)+''',
            "neurons_multiplier": '''+str(self.neurons_multiplier)+''',
            "num_neighbours": '''+str(self.num_neighbours)+''',
            "steps": '''+str(self.steps)+'''

          ''')
        if(should_break):
          break




  def init_neurons(self):
    num_neurons = len(self.cities) * self.neurons_multiplier
    centerx,centery = self.self_org_map.centeroidnp(np.array(self.cities))
    neurons = []
    for i in range(num_neurons):
      circ_x = centerx + self.init_neuron_radius * math.cos(hp.translate(i, 0, num_neurons, 0, math.pi*2))
      circ_y = centery + self.init_neuron_radius * math.sin(hp.translate(i, 0, num_neurons, 0, math.pi*2))
      neurons.append([circ_x, circ_y])
    return neurons


  def on_start_press(self):
    for i in range(self.epochs):
     self.neurons = self.self_org_map.run(self.neurons, self.cities, np.exp(-i/self.learning_rate_decay), self.lr_reduction_factor, self.num_neighbours, self.steps)

     if(i%100 == 0):
       self.num_neighbours -= 1

     self.ordered_cities = self.self_org_map.calculate_finished_path(self.neurons, self.cities)

     self.ordered_cities = self.self_org_map.enhance_finished_path(self.ordered_cities)

     self.re_mapped_cities = []
     for i in range(len(self.ordered_cities)):
      x = hp.translate(self.ordered_cities[i][0], 10, 800-10, self.min_x, self.max_x)
      y = hp.translate(self.ordered_cities[i][1], 10, 800-10, self.min_y, self.max_y)
      self.re_mapped_cities.append([x,y])
     self.re_mapped_cities = self.self_org_map.enhance_finished_path(self.re_mapped_cities)

    path_length = self.self_org_map.get_path_length(self.re_mapped_cities)
    optimal_path_length = self.optimalTSP[int(self.board-1)]
    if((((path_length / optimal_path_length)*100)-100) < 11):

     self.optimal_count += 1
     return False
    return True

    #  print("Board: ", self.board)
    #  print("Path length:", path_length)
    #  print("Optimal length:", optimal_path_length)
    #  print("percent above optimal:", ((path_length / optimal_path_length)*100)-100)
    #  print("\n")

if __name__ == '__main__':
    App()