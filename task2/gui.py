#!/usr/bin/env python
import tkinter as tk
import main

class App(tk.Frame):
  def __init__( self, parent):
    tk.Frame.__init__(self, parent)

    self.rect_size = 20
    self.grid()
    self.createWidgets()

    self.isStartet = False
    self.index = 0
    self.image = []
    self.task()

  def on_start_press(self):
    if(not self.isStartet):
      self.image = main.main()
      self._createCanvas(len(self.image), len(self.image[0].domain[0]))
      self.canvas.delete("all")
      self.isStartet = True


  def createWidgets(self):
    self.startButton = tk.Button(text="Start", command=lambda : self.on_start_press())
    self.startButton.grid()

    self.exitButton = tk.Button(text="Exit", command=lambda : exit())
    self.exitButton.grid()

  def _createCanvas(self, height, width):
    self.canvas = tk.Canvas(width = width * self.rect_size, height = height * self.rect_size,
                            bg = "grey" )
    self.canvas.grid(row=0, column=0, sticky='nsew')

  def show_board(self):
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
            
  def task(self):
    if(self.isStartet):
      self.show_board()
    self.after(500, self.task)  # reschedule event in 2 seconds


if __name__ == "__main__":
  root = tk.Tk()
  root.geometry( "700x500" )
  app = App(root)
  root.mainloop()
