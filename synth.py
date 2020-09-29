import gep
from ugen import *

def generate_gen_pset(lfos=False):
    pset = gep.PrimitiveSet()
    pset.add_function(blit, 2)
    pset.add_function(crossfm, 4)
    pset.add_function(fsine, 1)
    pset.add_function(phasor, 2)
    pset.add_function(rcosc, 2)
    pset.add_function(sineloop, 2)
    pset.add_function(supersaw, 3)
    if lfos:
        pset.add_function(sawuplfo, 2)
        pset.add_function(sawdownlfo, 2)
        pset.add_function(squarelfo, 2)
        pset.add_function(trilfo, 2)
        pset.add_function(pulselfo, 2)
        pset.add_function(bipulselfo, 2)
        pset.add_function(shlfo, 2)
        pset.add_function(modsinelfo, 2)
    return pset

def generate_proc_pset():
    pset = gep.PrimitiveSet()
    #pset.add_terminal("gen")
    #pset.add_function(disto, 3)
    #pset.add_function(delay, 3)
    pset.add_function(freeverb, 4)
    pset.add_function(chorus, 4)
    return pset

class GeneratorChromosome(gep.Chromosome):
    def __init__(self, n_genes, head_length, lfos=False):
        super(GeneratorChromosome, self).__init__(n_genes, generate_gen_pset(lfos), head_length, mix)
    
    '''
    def enforce_rules(self):
        for gene in self.genes:
            if not isinstance(gene.genome[0], gep.Function):
                gene.genome[0] = generate_gen_pset().choose_function()
    '''
    
    def get_tree(self):
        sub_funcs = [None] * self.n_genes
        for i in range(self.n_genes):
            sub_funcs[i] = "tanh(" + str(self.genes[i]) + ")"
        return self.link_func.__name__ + "([" + ", ".join(sub_funcs) + "])"

class ProcessorChromosome(gep.Chromosome):
    def __init__(self, n_genes, head_length):
        super(ProcessorChromosome, self).__init__(n_genes, generate_proc_pset(), head_length, mix)
    
    def enforce_rules(self):
        for gene in self.genes:
            if not isinstance(gene.genome[0], gep.Function):
                gene.genome[0] = generate_proc_pset().choose_function()
    
    def get_tree(self):
        sub_funcs = [None] * self.n_genes
        for i in range(self.n_genes):
            original_genome = self.genes[i].genome
            constrained_genome = original_genome[:]
            constrained_genome[1] = gep.Terminal("gen")
            self.genes[i].genome = constrained_genome
            sub_funcs[i] = "tanh(" + str(self.genes[i]) + ")"
            self.genes[i].genome = original_genome
        return self.link_func.__name__ + "([" + ", ".join(sub_funcs) + "])"

class Synth(gep.Individual):
    def __init__(self, gen_n_genes, gen_head_length, lfos=False):
        super(Synth, self).__init__()
        self.gen_chromosome = GeneratorChromosome(gen_n_genes, gen_head_length, lfos)
        self.chromosomes = [self.gen_chromosome]
    
    def get_patch(self):
        gen_tree = self.gen_chromosome.get_tree()
        gen = eval(gen_tree)
        return gen

def generate_synth_population(n):
    population = gep.Population(n)
    population.individuals = [Synth(4, 4) for i in range(n)]
    return population