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

## Changelog

Version|Changes
-|-
0.1|First working prototype
0.2|Tk gui, tanh compression added, ugens with inputs managed, more ugens

## TODO
- Implement more ugens.
- Create an exponential interpolation fitting the psychoacoustic frequency curve to constrain frequencies.
- Add manual elitism.
- Modify algorithm to check for empty synths and regenerate them to have only synth with a root function.
- Modify algorithm to check for audio frequencies in synths and regenerate them to have only synths with sound.
- Make a nice graphical interface.
- Develop a way to selectively inject ugens in genome to constrain a range of application.
- Individuals have chromosomes composed of multiple genomes mixed together.
- Individuals have 2 chromosomes : 1 for synthesis and 1 for signal processing.

## Interactions ideas

Assigning fitness :
- Manually assign a fitness.
- Select between : no reproduction, reproduce, reproduce a lot.

Selecting the primitive set :
- By selecting each manually.
- By assigning weights to families of ugens. Needs a select_primitive function for generation and mutation.

Keyboard mode : 
- Plug a MIDI keyboard and constrain the synths to have a midi to frequency converter.

## References

- A. Allik. Gene expression synthesis.
- C. Ferreira. Gene expression programming: a new adaptive algorithm for solving problems.
- C. Ferreira. Gene Expression Programming: Mathematical Modeling by an Artificial Intelligence.
