import tkinter as tk
from functools import partial
import globals
import gep
from ugen import *

def pause_synth():
    if globals.synth is not None and isinstance(globals.synth, pyo.PyoObject):
        globals.synth.stop()
        
def reproduce():
    pause_synth()
    globals.population = gep.get_next_generation(globals.population)

def set_fitness(id, fitness):
    globals.population.individuals[id - 1].set_fitness(fitness)

# GUI UTILITIES

class Cell(tk.Frame):
    def __init__(self, id, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.id = id
        self.cellbutton = tk.Button(
            text = str(id),
            height = 1,
            width = 10,
            bg = "black",
            fg = "white",
            activebackground = "white",
            activeforeground = "black",
            master = self,
            command = self.play_synth_and_update_synth_print)
        self.fitness_frame = tk.Frame(
            master = self,
            bd = 1)
        self.fitness_zero = tk.Button(
            text = "0",
            width = 1,
            height = 1,
            bg = "black",
            fg = "white",
            activebackground = "white",
            activeforeground = "black",
            master = self.fitness_frame,
            command = partial(set_fitness, id, 0))
        self.fitness_one = tk.Button(
            text = "1",
            width = 1,
            height = 1,
            bg = "black",
            fg = "white",
            activebackground = "white",
            activeforeground = "black",
            master = self.fitness_frame,
            command = partial(set_fitness, id, 1))
        self.fitness_four = tk.Button(
            text = "4",
            width = 1,
            height = 1,
            bg = "black",
            fg = "white",
            activebackground = "white",
            activeforeground = "black",
            master = self.fitness_frame,
            command = partial(set_fitness, id, 4))
        self.cellbutton.pack()
        self.fitness_frame.pack()
        self.fitness_zero.pack(side=tk.LEFT)
        self.fitness_one.pack(side=tk.LEFT)
        self.fitness_four.pack(side=tk.LEFT)
    
    def play_synth_and_update_synth_print(self):
        print("==============")
        pause_synth()
        print(str(globals.population.individuals[self.id - 1]))
        globals.synth = tanh(globals.population.individuals[self.id - 1].get_patch())
        globals.synth.out()
        self.parent.parent.update_synth_print(self.id)
    
class CellGrid(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.cells = [None]*16
        for i in range(4):
            for j in range(4):
                id = (4*i) + j + 1
                self.cells[id - 1] = Cell(
                    id,
                    self,
                    bg="white",
                    borderwidth=1,
                    highlightbackground="white",
                    highlightcolor = "white")
                self.cells[id - 1].grid(row=i, column=j)

# GUI MAIN

class Gui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.synth_print = tk.StringVar(value="")
        self.reproduce_button = tk.Button(
            text = "REPRODUCE",
            height=1,
            activebackground = "white",
            activeforeground = "black",
            bg = "black",
            fg = "white",
            master = parent,
            command = reproduce)
        self.text_box = tk.Label(
            textvariable = self.synth_print,
            width = 120,
            height = 25,
            bg = "black",
            fg = "white",
            bd = 1,
            highlightbackground="white",
            justify=tk.LEFT,
            anchor="nw",
            master = parent,
            wraplength=1000)
        self.cellgrid = CellGrid(self, bg="black")
        self.reproduce_button.pack()
        self.cellgrid.pack()
        self.text_box.pack()
    
    def update_synth_print(self, id):
        to_print = []
        to_print.append("Individual n°" + str(id))
        to_print.append("Fitness : " + str(globals.population.individuals[id - 1].fitness))
        to_print.append(repr(globals.population.individuals[id - 1]))
        self.synth_print.set("\n".join(to_print))