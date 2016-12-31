## Installation

This solver requires Python 3 and `numpy`.

To use the GUI you will need tkinter, the default python GUI library. On debian/Ubuntu: `sudo apt-get install python3-tk`).

Note: You can use the program without GUI with the flag `--nogui`.

## Use

Examples

```
# print the help
$ .src/solver.py -h

# read the standard input
$ .src/solver.py -s

# solve an example (number between 0 and 4) and show all the steps
$ .src/solver.py -e 3 -p

# read the standard input and solve hide the steps (faster)
$ .src/solver.py -s -f

# disable the GUI
$ .src/solver.py -e 2 -n
```

## Démarche

J'ai choisi de coder tout le programme pour comprendre comment chaque élément fonctionne.

Le coeur du programme est dans la fonction `solver`.

L'arbre est modélisé par une pile Last In First Out qui permet de continuer l'exploration de l'arbre lorsque l'on rencontre
une impasse.

## Misc

The shapes are :

![shapes](tuiles.svg)

Link to the [TP](http://www-desir.lip6.fr/~durrc/Iut/optim/t/dm1-connect).


