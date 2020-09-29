import random
import copy

class PrimitiveSet:
    def __init__(self):
        self.functions = []
        self.terminals = []
    
    def add_function(self, function, arity):
        self.functions.append(Function(function, arity))
    
    def add_terminal(self, variable):
        self.terminals.append(Terminal(variable))
    
    def choose_function(self):
        return random.choice(self.functions)
    
    def choose_terminal(self):
        if random.random() < 0.5 or not self.terminals:
            return Terminal(random.random())
        else:
            return random.choice(self.terminals)

class Function:
    def __init__(self, func, arity):
        self.func = func
        self.arity = arity
    
    def format(self, *args):
        args = args[:self.arity]
        return (self.func.__name__ + '(' + ', '.join(map(str, args)) + ')')

    def __str__(self):
        return self.func.__name__

    def __repr__(self):
        return self.func.__name__

class Terminal:
    def __init__(self, value):
        self.value = value
        self.arity = 0
    
    def format(self):
        return str(self.value)
    
    def __str__(self):
        if isinstance(self.value, str):
            return self.value
        else:
            return str(round(self.value, 3))

    def __repr__(self):
        if isinstance(self.value, str):
            return self.value
        else:
            return str(round(self.value, 3))


def generate_genome(pset, head_length, enforce_root_func=False):
    functions = pset.functions

    # Get max arity
    n_max = max(p.arity for p in functions)
    # Get tail length
    tail_length = head_length * (n_max - 1) + 1
    # Initialize genome
    genome = [None] * (head_length + tail_length)
    # Generate head part (functions and terminals)
    start = 1 if enforce_root_func else 0
    if enforce_root_func:
        genome[0] = pset.choose_function()
    for i in range(start,head_length):
        if random.random() < 0.5:
            genome[i] = pset.choose_function()
        else:
            genome[i] = pset.choose_terminal()
    # Generate tail part (only terminals)
    for i in range(head_length, head_length + tail_length):
        genome[i] = pset.choose_terminal()
    return genome

class Gene:
    def __init__(self, pset, head_length, enforce_root_func=False):
        self._head_length = head_length
        self.genome = generate_genome(pset, head_length, enforce_root_func)

    def get_kexpression(self):
        genome = self.genome
        expr = [genome[0]]
        i = 0
        j = 1
        while i < len(expr):
            for _ in range(genome[i].arity):
                expr.append(genome[j])
                j += 1
            i += 1
        return expr

    def __str__(self):
        kexpr = self.get_kexpression()
        # Start by the last item of the kexpression
        i = len(kexpr) - 1
        # Iterate while we're not at the first index
        while i >= 0:
            # If the item is a function
            if kexpr[i].arity > 0:
                f = kexpr[i]
                args = []
                # For the number of arity
                for _ in range(f.arity):
                    # Remove the last element
                    element = kexpr.pop()
                    # If this element is a string (already formatted)
                    if isinstance(element, str):
                        # Append it to the args of the current function item
                        args.append(element)
                    else:
                        # Else, it's a terminal and append it to the args of the current function item
                        args.append(element.format())
                # When all args for this function has been acquired, format
                kexpr[i] = f.format(*reversed(args))
            i -= 1
        # If the root is formatted, return, else format the root
        return kexpr[0] if isinstance(kexpr[0], str) else kexpr[0].format()

    def __repr__(self):
        fmt = "{:<5}|"*len(self.genome)
        return fmt.format(*[str(prim) for prim in self.genome])

class Chromosome:
    def __init__(self, n_genes, pset, head_length, link_func):
        self.n_genes = n_genes
        self.pset = pset
        self.head_length = head_length
        self.link_func = link_func
        self.genes = None
        self.init_genes()
    
    def init_genes(self):
        self.genes = [Gene(self.pset, self.head_length) for _ in range(self.n_genes)]
    
    def enforce_rules(self):
        pass
    
    def __str__(self):
        print(str(self.genes))
    
    def __repr__(self):
        return "\n".join(["Gene " + str(i) + " : " + repr(gene) + "\n>>> " + str(gene) for i, gene in enumerate(self.genes)])

class Individual:
    def __init__(self):
        self.chromosomes = None
        self.fitness = 0.1
        self.elite = False
    
    def set_fitness(self, fitness):
        self.fitness = fitness
    
    def __str__(self):
        return str(self.chromosomes)
    
    def __repr__(self):
        return str(self.chromosomes)

class Population:
    def __init__(self, n):
        self.n = n
        self.individuals = None

def select_wheel(population):
    # Roulette wheel selection (fitness based)
    total_fitness = sum([individual.fitness for individual in population.individuals])
    selected_individuals = []
    elites = [individual for individual in population.individuals if individual.elite]
    for _ in range(population.n - len(elites)):
        choice = random.uniform(0, total_fitness)
        i = 0
        for individual in population.individuals:
            i += individual.fitness
            if i >= choice:
                selected_individuals.append(copy.deepcopy(individual))
                break
    for individual in selected_individuals:
        individual.fitness = 0.1
    selected_population = Population(population.n)
    selected_population.individuals = elites
    selected_population.individuals += selected_individuals
    return(selected_population)

def mutate(population, mutations_per_individual=2):
    # Basic mutation of primitives
    individuals = population.individuals
    n_chromosomes = len(individuals[0].chromosomes)
    for i in range(n_chromosomes):
        pset = individuals[0].chromosomes[i].pset
        head_length = individuals[0].chromosomes[i].head_length
        n_genes = individuals[0].chromosomes[i].n_genes
        max_arity = max(p.arity for p in pset.functions)
        tail_length = head_length * (max_arity - 1) + 1
        for individual in individuals:
            chromosome = individual.chromosomes[i]
            for _ in range(mutations_per_individual):
                selected_gene = random.randint(0, n_genes - 1)
                mutation_index = random.randint(0, head_length + tail_length - 1)
                if mutation_index < head_length:
                    # In the head, mutate function or terminals
                    if random.random() < 0.5:
                        chromosome.genes[selected_gene].genome[mutation_index] = pset.choose_function()
                    else:
                        chromosome.genes[selected_gene].genome[mutation_index] = pset.choose_terminal()
                else:
                    # In the tail, mutate terminals
                    chromosome.genes[selected_gene].genome[mutation_index] = pset.choose_terminal()

def invert(population, p=0.1):
    # Inversion of portions of genome
    individuals = population.individuals
    n_chromosomes = len(individuals[0].chromosomes)
    for i in range(n_chromosomes):
        head_length = individuals[0].chromosomes[i].head_length
        if head_length > 2:
            selected_individuals = random.choices(individuals, k=int(p * population.n))
            for individual in selected_individuals:
                chromosome = individual.chromosomes[i]
                selected_gene = random.randint(0, chromosome.n_genes - 1)
                start = random.randint(0, head_length - 2)
                stop = random.randint(start+1, head_length)
                chromosome.genes[selected_gene].genome[start: stop+1] = reversed(chromosome.genes[selected_gene].genome[start: stop+1])

def transpose_is(population, p=0.1):
    # Non-root transposition
    individuals = population.individuals
    n_chromosomes = len(individuals[0].chromosomes)
    for i in range(n_chromosomes):
        pset = individuals[0].chromosomes[i].pset
        head_length = individuals[0].chromosomes[i].head_length
        n_genes = individuals[0].chromosomes[i].n_genes
        max_arity = max(p.arity for p in pset.functions)
        tail_length = head_length * (max_arity - 1) + 1
        gene_length = head_length + tail_length
        if head_length > 2:
            selected_individuals = random.choices(individuals, k=int(p * population.n))
            for individual in selected_individuals:
                chromosome = individual.chromosomes[i]
                selected_gene = random.randint(0, n_genes - 1)
                is_length = random.randint(0, head_length - 1)
                start = random.randint(0, gene_length - is_length)
                stop = start + is_length
                iseq = chromosome.genes[selected_gene].genome[start:stop + 1] 
                insertion_point = random.randint(1, head_length - is_length)
                chromosome.genes[selected_gene].genome[insertion_point:insertion_point + is_length + 1] = iseq

def transpose_ris(population, p=0.1):
    # Root transposition
    individuals = population.individuals
    n_chromosomes = len(individuals[0].chromosomes)
    for i in range(n_chromosomes):
        pset = individuals[0].chromosomes[i].pset
        head_length = individuals[0].chromosomes[i].head_length
        n_genes = individuals[0].chromosomes[i].n_genes
        max_arity = max(p.arity for p in pset.functions)
        tail_length = head_length * (max_arity - 1) + 1
        gene_length = head_length + tail_length
        if head_length > 2:
            selected_individuals = random.choices(population.individuals, k=int(p * population.n))
            for individual in selected_individuals:
                chromosome = individual.chromosomes[i]
                selected_gene = random.randint(0, n_genes - 1)
                function_idx = [i for i, p in enumerate(chromosome.genes[selected_gene].genome) if isinstance(p, Function)]
                if not function_idx:
                    continue
                start = random.choice(function_idx)
                is_length = random.randint(2, head_length - 1)
                riseq = chromosome.genes[selected_gene].genome[start:start+is_length]
                chromosome.genes[selected_gene].genome[0:is_length] = riseq    

def onep_recombine(population, p=0.1):
    # One point recombination
    individuals = population.individuals
    n_chromosomes = len(individuals[0].chromosomes)
    for i in range(n_chromosomes):
        pset = individuals[0].chromosomes[i].pset
        head_length = individuals[0].chromosomes[i].head_length
        n_genes = individuals[0].chromosomes[i].n_genes
        max_arity = max(p.arity for p in pset.functions)
        tail_length = head_length * (max_arity - 1) + 1
        gene_length = head_length + tail_length
        # Choose parents1
        parents1 = random.choices(individuals, k=int(p * population.n))
        for parent1 in parents1:
            # Select parent 2 different from parent1
            while True:
                parent2 = random.choice(individuals)
                if parent1 != parent2:
                    break
            # Choose recomb point and genes for each parent chromosomes
            recomb_point = random.randint(0, gene_length - 1)
            selected_gene1 = random.randint(0, n_genes - 1)
            selected_gene2 = random.randint(0, n_genes - 1)
            # Buffer swap genomes
            buffer = parent1.chromosomes[i].genes[selected_gene1].genome[recomb_point:]
            parent1.chromosomes[i].genes[selected_gene1].genome[recomb_point:] = parent2.chromosomes[i].genes[selected_gene2].genome[recomb_point:]
            parent2.chromosomes[i].genes[selected_gene2].genome[recomb_point:] = buffer

def twop_recombine(population, p=0.1):
    # Two point recombination
    individuals = population.individuals
    n_chromosomes = len(individuals[0].chromosomes)
    for i in range(n_chromosomes):
        pset = individuals[0].chromosomes[i].pset
        head_length = individuals[0].chromosomes[i].head_length
        n_genes = individuals[0].chromosomes[i].n_genes
        max_arity = max(p.arity for p in pset.functions)
        tail_length = head_length * (max_arity - 1) + 1
        gene_length = head_length + tail_length
        # Choose parents1
        parents1 = random.choices(individuals, k=int(p * population.n))
        for parent1 in parents1:
            # Select parent 2 different from parent1
            while True:
                parent2 = random.choice(individuals)
                if parent1 != parent2:
                    break
            # Choose recomb start and end
            recomb_point = random.randint(0, gene_length - 1)
            recomb_end = random.randint(recomb_point, gene_length - 1)
            selected_gene1 = random.randint(0, n_genes - 1)
            selected_gene2 = random.randint(0, n_genes - 1)
            # Buffer swap genome
            buffer = parent1.chromosomes[i].genes[selected_gene1].genome[recomb_point:recomb_end+1]
            parent1.chromosomes[i].genes[selected_gene1].genome[recomb_point:recomb_end+1] = parent2.chromosomes[i].genes[selected_gene2].genome[recomb_point:recomb_end+1]
            parent2.chromosomes[i].genes[selected_gene2].genome[recomb_point:recomb_end+1] = buffer

def gene_recombine(population, p=0.1):
    # Exchange genes between chromosomes
    individuals = population.individuals
    n_chromosomes = len(individuals[0].chromosomes)
    for i in range(n_chromosomes):
        n_genes = individuals[0].chromosomes[i].n_genes
        # Choose parents1
        parents1 = random.choices(individuals, k=int(p * population.n))
        for parent1 in parents1:
            # Select parent 2 different from parent1
            while True:
                parent2 = random.choice(individuals)
                if parent1 != parent2:
                    break
            # Choose genes to swap
            selected_gene1 = random.randint(0, n_genes - 1)
            selected_gene2 = random.randint(0, n_genes - 1)
            # Buffer swap genes
            buffer = parent1.chromosomes[i].genes[selected_gene1].genome[:]
            parent1.chromosomes[i].genes[selected_gene1].genome = parent2.chromosomes[i].genes[selected_gene2].genome[:]
            parent2.chromosomes[i].genes[selected_gene2].genome = buffer

def enforce_rules(population):
    for individual in population.individuals:
        for chromosome in individual.chromosomes:
            chromosome.enforce_rules()

def get_next_generation(population):
    # User evaluates fitness
    selected_population = select_wheel(population)
    mutate(selected_population)
    invert(selected_population)
    transpose_is(selected_population)
    transpose_ris(selected_population)
    onep_recombine(selected_population)
    twop_recombine(selected_population)
    gene_recombine(selected_population)
    enforce_rules(selected_population)
    return selected_population