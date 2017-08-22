#!/usr/bin/env python
import tkinter as tk
import main

class Application(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.grid()
    self.createWidgets()
    self._createCanvas()
    self.rectx0 = 0
    self.recty0 = 0
    self.rectx1 = 100
    self.recty1 = 100

  def createWidgets(self):
    self.startButton = tk.Button(text="Start", command=lambda : main.main())
    self.startButton.grid()

  def _createCanvas(self):
    self.canvas = tk.Canvas(width = 800, height = 400,
                            bg = "white" )
    self.canvas.grid(row=0, column=0, sticky='nsew')

  def show_board(self):
    for i in range(6):
          for j in range(6):
            self.rect = self.canvas.create_rectangle(
              self.rectx0, self.recty0, self.rectx0, self.recty0, fill="#4eccde")

app = Application()
app.master.title('AIprog1')

def task():
  #curr_board = main.current_board
  app.show_board()

  app.after(100, task)  # reschedule event in 2 seconds

app.after(100, task)



app.mainloop()
