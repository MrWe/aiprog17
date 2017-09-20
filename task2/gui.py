#!/usr/bin/env python
import tkinter as tk
import main
import ast


class App(tk.Frame):
  def __init__( self, parent):
    tk.Frame.__init__(self, parent)

    self.rect_size = 20
    self.grid()
    self.createWidgets()
    self.see_pop_in = False
    self.isStartet = False
    self.index = 0
    self.partial_image_dict = {}
    self.partial_image = []
    self.image = []
    self.path = []
    self.task()

  def on_start_press(self):
    if(not self.isStartet):
      self.image = main.main()
      if hasattr(self.image, 'parent'):
        while (self.image.parent):
          self.path.insert(0, self.image.row_nodes)
          self.image = self.image.parent
        self.path.insert(0, self.image.row_nodes)
      print("The total number of search nodes on the path from the root to the solution state: ", len(self.path))
      self._createCanvas(len(self.image.row_nodes), len(self.image.row_nodes[0].domain[0]))
      self.canvas.delete("all")
      self.isStartet = True


  def see_path(self):
    temp = []
    f = open('workfile', 'r')
    for l in f:
      if l.strip() != "":
        temp.append(ast.literal_eval(l))
      else:
        if(not len(temp) == 0):
          self.partial_image.append(temp)
          temp = []
    self.see_pop_in = True

  def createWidgets(self):
    self.startButton = tk.Button(text="Start", command=lambda : self.on_start_press())
    self.startButton.grid()

    self.path = tk.Button(text="See path", command=lambda : self.see_path())
    self.path.grid()

    self.exitButton = tk.Button(text="Exit", command=lambda : exit())
    self.exitButton.grid()



  def _createCanvas(self, height, width):
    self.canvas = tk.Canvas(width = width * self.rect_size, height = height * self.rect_size,
                            bg = "grey" )
    self.canvas.grid(row=0, column=0, sticky='nsew')

  def show_board(self):
    if(self.path):
      self.canvas.delete("all")
      self.image = self.path[self.index]
      for i in range(len(self.image)):
        for j in range(len(self.image[i].domain[0])):
            if(self.image[i].domain[0][j] == 0):
              fill = "#ff4be6"
            else:
              fill = "#000000"
            x0, y0 = j * self.rect_size, i * self.rect_size
            x1, y1 = x0 + self.rect_size-1, y0 + self.rect_size-1

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=1, state='disabled')
    else:
      self.image = self.image.row_nodes
      if(len(self.image) != 0):
        self.canvas.delete("all")
        for i in range(len(self.image)):
          for j in range(len(self.image[i].domain[0])):
              if(self.image[i].domain[0][j] == 0):
                fill = "#ff4be6"
              else:
                fill = "#000000"
              x0, y0 = j * self.rect_size, i * self.rect_size
              x1, y1 = x0 + self.rect_size-1, y0 + self.rect_size-1

              self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=1, state='disabled')

  def show_partial(self):
    if(self.partial_image):
      self.canvas.delete("all")
      points = self.partial_image[self.index]
      for i in range(len(points)):

        keys = points[i]
        for j in range(len(self.image[i].domain[0])):
          if(j in keys):
            if(self.image[i].domain[0][j] == 0):
              fill = "#ff4be6"
            else:
              fill = "#000000"
            x0, y0 = j * self.rect_size, i * self.rect_size
            x1, y1 = x0 + self.rect_size-1, y0 + self.rect_size-1

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=1, state='disabled')

  def task(self):
    after = 1000
    if(self.isStartet):
      if(self.see_pop_in):
        after = 20
        self.show_partial()
        if(self.index != len(self.partial_image)-1):
             self.index += 1
      else:
        self.show_board()
        if(self.index != len(self.path)-1):
          self.index += 1


    self.after(after, self.task)


if __name__ == "__main__":
  root = tk.Tk()
  root.geometry( "700x500" )
  app = App(root)
  root.mainloop()
