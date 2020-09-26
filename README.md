# osc_breeder

A gene expression programming based evolutionary audio synthesizer by Valentin Lageard.

## Requirements

- pyo : `sudo pip3 install pyo`

## Usage

Launch the notebook and evaluate all cells.

In the last cell, a modest command interface allows you to :
- [1-16] : Listen individual synth from 1 to 16.
- [s] : Stop the current playing synth.
- [r] : Reproduce this population to get the new population.
- [1-16]=[0-4] : Assign fitness [0-4] to the individual [1-16]

Usually you'll want to listen to all synth in a generation, assign them fitnesses, then reproduce to get a new generation.

## Architecture

### Global

1. Generate n ugen graphs.
2. Let the user select the favorite ugen graphs.
3. Regenerate n ugen graphs based on user selection and genetic operators.

### Audio

pyo ugens are wrapped in functions allowing to control how the genome is expressed as parameters of pyo ugens.

### Gene Expression Programming
Implemented in `gep.py`.

To get next generation :
1. Select wheel.
2. Primitive mutation.
3. Segment inversion.
4. Non-root segment transposition.
5. Root segment transposition.
6. 1 point recombination.
7. 2 point recombination. 

## References

- A. Allik. Gene expression synthesis.
- C. Ferreira. Gene expression programming: a new adaptive algorithm for solving problems.
- C. Ferreira. Gene Expression Programming: Mathematical Modeling by an Artificial Intelligence.
