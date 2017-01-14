## Installation
This solver requires Python 3 and `numpy`.

To use the GUI you will need tkinter, the default python GUI library. On Debian/Ubuntu: `sudo apt-get install python3-tk`.

Note: You can use the program without GUI with the flag `--nogui`, or `-n`.

## Examples

```
# prints the help
$ ./src/solver.py -h

# reads the standard input (-s)
$ cat cadeau | ./src/solver.py -s

# reads the standard input and solves it fast (-f, ie GUI updates only at the end), with arc-consistency (-a)
$ cat cadeau | ./src/solver.py -sfa

# solves an example (-e, number between 0 and 4) and shows all the steps (-p, voluntarily slow)
$ ./src/solver.py -e 3 -p

# reads the standard input, without GUI (-n) and with forward check (-c)
$ ./src/solver.py -snc
```

========================================
========================================

## Method
J'ai choisi de coder tout le programme pour comprendre comment chaque élément fonctionne.

Je ne recherche pas qu'une ou deux solution mais je les recherches toutes.

L'arbre est modélisé par une pile Last In First Out qui permet de continuer l'exploration de l'arbre lorsque l'on rencontre
une impasse.

### Improvements
#### Forward Check

#### Arc-Consistency

## Results

Time to find all the solutions of the examples grids (without GUI) **in ms**:


We observe that forward check is either really badly implemented, either not a good idea for this specific type of problem.


| examples | number of solutions | dimensions |     basic       |  forward check   | arc-consistency |
|----------|---------------------|------------|-----------------|------------------|-----------------|
| 0        |          0          |     3x3    |        2        |         2        |        3        |
| 1        |          1          |     3x3    |        2        |         3        |        2        |
| 2        |          1          |     5x5    |        18       |        27        |        22       |
| 3        |          8          |     5x5    |        20       |        35        |        36       |
| 4        |          2          |     7x9    |        60       |      500 (!)     |        75       |
| gift     |          1          |    19x20   |      7 750      |  several minutes |      12 600     |



## Code organization
Le coeur du programme est dans la fonction `solver`.

========================================
========================================

## Misc
The shapes are : ![shapes](tuiles.svg)

Link to the [TP](http://www-desir.lip6.fr/~durrc/Iut/optim/t/dm1-connect).


