import pyo
import gep
from ugen import *
import globals

# HANDLERS

def pause_synth():
    if globals.synth is not None and isinstance(globals.synth, pyo.PyoObject):
        globals.synth.stop()

def play_synth(id):
    pause_synth()
    globals.synth = eval("tanh(" + str(globals.population.individuals[int(id) - 1].gene) + ")")
    if isinstance(globals.synth, pyo.PyoObject):
        globals.synth.out()

def assign_fitness(id, fitness):
    globals.population.individuals[int(id) - 1].fitness = float(fitness)

def reproduce():
    globals.population = gep.get_next_generation(globals.population)

# Handler : Assign elite
