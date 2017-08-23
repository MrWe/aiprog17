#!/usr/bin/env python
import tkinter as tk
import main
from car import Car
import random
import time

class App(tk.Frame):
  def __init__( self, parent):
    tk.Frame.__init__(self, parent)

    self.rect_size = 50
    self.grid()
    self.createWidgets()
    self._createCanvas()
    self.isStartet = False
    self.index = 0
    self.path = []
    self.task()

  def on_start_press(self):
    if(not self.isStartet):
      self.reverse_path = main.main()
      while (self.reverse_path.parent):
          self.path.insert(0, self.reverse_path)
          self.reverse_path = self.reverse_path.parent
      self.path.insert(0, self.reverse_path)
      self.isStartet = True
      self.canvas.delete("all")

  def on_move_press(self):
    if(self.index == len(self.path)-1):
      self.index = 0
    else:
      self.index += 1
    self.canvas.delete("all")


  def createWidgets(self):
    self.startButton = tk.Button(text="Start", command=lambda : self.on_start_press())
    self.startButton.grid()

    self.moveButton = tk.Button(text="Step", command=lambda : self.on_move_press())
    self.moveButton.grid()

  def _createCanvas(self):
    self.canvas = tk.Canvas(width = 6 * self.rect_size, height = 6 * self.rect_size,
                            bg = "grey" )
    self.canvas.grid(row=0, column=0, sticky='nsew')

  def show_board(self):
    if(self.path):
      self.canvas.delete("all")
      for t in range(len(self.path[self.index].cars)):
        car = self.path[self.index].cars[t]
        if(t == 0):
          fill = "#ff0000"
        else:
          fill = "#000000"
        if(car.O == 0):
          coords = (car.X*self.rect_size+4, car.Y*self.rect_size+4, car.X*self.rect_size+(self.rect_size*car.S), car.Y*self.rect_size+self.rect_size)
        elif(car.O == 1):
          coords = (car.X*self.rect_size+4, car.Y*self.rect_size+4, car.X*self.rect_size+self.rect_size, car.Y*self.rect_size+(self.rect_size*car.S))
        self.canvas.create_rectangle(coords, fill=fill, width=1, state='disabled')

    '''
    TODO: Try to make small rectangles on board in between cars
    for r in range(6, -1, -1):
      for c in range(6):
        coords = (c*(self.rect_size/2)+4, r*(self.rect_size/2)+4, c*self.rect_size+self.rect_size, r*self.rect_size+self.rect_size)
        self.canvas.create_rectangle(coords, fill="#515151", width=1, state='disabled')
    '''

  def task(self):
    if(self.isStartet):
      self.show_board()
      if(self.index == len(self.path)-1):
        self.index = 0
      else:
        self.index += 1
    self.after(500, self.task)  # reschedule event in 2 seconds


if __name__ == "__main__":
  root = tk.Tk()
  root.geometry( "700x500" )
  app = App(root)
  root.mainloop()
