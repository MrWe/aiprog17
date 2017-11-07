#!/usr/bin/env python
import tkinter as tk
import som as som
import read_file as rf
import math
import helper as hp


class App(tk.Frame):
  def __init__( self, parent):
    tk.Frame.__init__(self, parent)

    self.width = 500
    self.height = 500
    self.grid()
    self.createWidgets()
    self._createCanvas()


  def restart(self):
    self.init_neuron_radius = 50
    self.learning_rate = 0.9
    self.epochs = 500
    self.neurons_multiplier = 3
    self.num_neighbours = 20
    self.self_org_map = som
    self.cities = rf.read_file('data/'+ self.entry.get() + '.txt', self.width, self.height)
    self.neurons = self.init_neurons()
    self.draw_points(self.cities)
    self.on_start_press()


  #NOTE: gui is looked until this is finished
  def on_start_press(self):
    print(self.entry.get())
    for i in range(self.epochs):
      self.neurons = self.self_org_map.run(self.neurons, self.cities, self.learning_rate, self.num_neighbours)
      root.update()
      self.show_board(self.neurons)
      self.learning_rate *= 0.995


  def init_neurons(self):
    num_neurons = len(self.cities) * self.neurons_multiplier
    neurons = []
    for i in range(num_neurons):
      circ_x = self.width/2 + self.init_neuron_radius * math.cos(hp.translate(i, 0, num_neurons, 0, math.pi*2))
      circ_y = self.height/2 + self.init_neuron_radius * math.sin(hp.translate(i, 0, num_neurons, 0, math.pi*2))
      neurons.append([circ_x, circ_y])
    return neurons

  def createWidgets(self):
    self.startButton = tk.Button(text="Restart", command=lambda : self.restart())
    self.startButton.grid()

    self.exitButton = tk.Button(text="Exit", command=lambda : exit())
    self.exitButton.grid()

    self.entry = tk.Entry()
    self.entry.pack()
    self.entry.insert(0,'1')
    self.entry.grid()


  def _createCanvas(self):
    self.canvas = tk.Canvas(width = self.width, height = self.height,
                            bg = "grey" )
    self.canvas.grid(row=0, column=0, sticky='nsew')


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
  root.geometry( "1000x1000" )
  app = App(root)
  root.mainloop()
