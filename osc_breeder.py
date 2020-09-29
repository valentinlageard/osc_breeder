import gep
import pyo
import gui
import tkinter as tk
from ugen import *
import globals
import synth as sy

# UTILITIES

# Audio server
server = pyo.Server(sr=22050, buffersize=1024).boot() # Boot the audio server
server.start() # Start the audio server
#server.stop() # Stop the audio server

# Initialize population
globals.population = sy.generate_synth_population(16)


# Start GUI
globals.root = tk.Tk()
globals.root.configure(bg="black")
gui.Gui(globals.root).pack()
globals.root.mainloop()