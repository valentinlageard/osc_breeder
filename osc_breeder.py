import gep
import pyo
import gui
import tkinter as tk
from ugen import *
import globals

# UTILITIES

def generate_pset():
    pset = gep.PrimitiveSet()
    #pset.add_function(blit, 2)
    #pset.add_function(crossfm, 4)
    #pset.add_function(fsine, 1)
    pset.add_function(phasor, 2)
    pset.add_function(rcosc, 2)
    #pset.add_function(sineloop, 2)
    pset.add_function(supersaw, 3)
    #pset.add_function(sawuplfo, 2)
    #pset.add_function(sawdownlfo, 2)
    #pset.add_function(squarelfo, 2)
    #pset.add_function(trilfo, 2)
    #pset.add_function(pulselfo, 2)
    #pset.add_function(bipulselfo, 2)
    pset.add_function(shlfo, 2)
    #pset.add_function(modsinelfo, 2)
    pset.add_function(disto, 3)
    pset.add_function(delay, 3)
    pset.add_function(freeverb, 4)
    pset.add_function(chorus, 4)
    return pset

# Audio server
server = pyo.Server(sr=22050, buffersize=1024).boot() # Boot the audio server
server.start() # Start the audio server
#server.stop() # Stop the audio server

# Initialize pset and population
globals.pset = generate_pset()
globals.population = gep.Population()
globals.population.generate(16, globals.pset, 16)

# Start GUI
globals.root = tk.Tk()
globals.root.configure(bg="black")
gui.Gui(globals.root).pack()
globals.root.mainloop()