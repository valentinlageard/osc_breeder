# osc_breeder

A gene expression evolutionary synthesizer.

## Problématiques

Comment encoder un graph dans une string ?

Quel framework d'ugen utiliser ?
- pyo ?

## Function set

Pyo class | Symbol | Selected args
-|-|-
FastSine||freq, initphase, mul, add
FM||carrier, ration, index, mul, add
LFO||freq, sharp, type, mul, add

## Architecture

1. Generate n ugen graphs.
2. Let the user select the favorite ugen graphs.
3. Regenerate n ugen graphs based on user selection.

Encodage/Décodage : 
`geno_to_pheno` : Fonction traduisant le phénotype (string python décrivant le générateur à executer) en génotype (???).
`pheno_to_geno` : Fonction traduisant le génotype (???) en phénotype.

Types de mutations (opèrent sur les génotypes) :
- Ajout
- Suppression
- ???

## References

- A. Allik. Gene expression synthesis.
- C. Ferreira. Gene expression programming: a new adaptive algorithm for solving problems.
- C. Ferreira. Gene Expression Programming: Mathematical Modeling by an Artificial Intelligence.
