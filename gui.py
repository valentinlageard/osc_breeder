import tkinter as tk
from functools import partial
import handler
import globals

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
            command = partial(handler.assign_fitness, self.id, 0))
        self.fitness_one = tk.Button(
            text = "1",
            width = 1,
            height = 1,
            bg = "black",
            fg = "white",
            activebackground = "white",
            activeforeground = "black",
            master = self.fitness_frame,
            command = partial(handler.assign_fitness, self.id, 1))
        self.fitness_four = tk.Button(
            text = "4",
            width = 1,
            height = 1,
            bg = "black",
            fg = "white",
            activebackground = "white",
            activeforeground = "black",
            master = self.fitness_frame,
            command = partial(handler.assign_fitness, self.id, 4))
        self.cellbutton.pack()
        self.fitness_frame.pack()
        self.fitness_zero.pack(side=tk.LEFT)
        self.fitness_one.pack(side=tk.LEFT)
        self.fitness_four.pack(side=tk.LEFT)
    
    def play_synth_and_update_synth_print(self):
        handler.play_synth(self.id)
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
            command = handler.reproduce)
        self.text_box = tk.Label(
            textvariable = self.synth_print,
            width = 80,
            height = 18,
            bg = "black",
            fg = "white",
            bd = 1,
            highlightbackground="white",
            master = parent,
            wraplength=600)
        self.cellgrid = CellGrid(self, bg="black")
        self.reproduce_button.pack()
        self.cellgrid.pack()
        self.text_box.pack()
    
    def update_synth_print(self, id):
        to_print = [None, None, None, None]
        to_print[0] = ("=" * 15) + "GENOTYPE" + ("=" * 15)
        to_print[1] = repr(globals.population.individuals[id - 1].gene.genome)
        to_print[2] = ("=" * 15) + "PHENOTYPE" + ("=" * 15)
        to_print[3] = str(globals.population.individuals[id - 1].gene)
        self.synth_print.set("\n".join(to_print))