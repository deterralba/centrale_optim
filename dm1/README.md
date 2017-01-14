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

## Approach

I chose to start from scratch.
**Conclusion**: I would not do it twice! A general purpose solver may be a bit less intuitive to use but allows optimizations and adding new constrains more easily than a home made, problem specific solver. Nevertheless it was interesting and I learned a lot.

Note: the solver doesn't look for one or two solutions but go through the entire tree and find them all, hence may be slower than other solvers.

### Implementation details

The exploration tree is represented by a FILO stack. The basic algorithm is:

1. start with an empty grid, find and store the domain of each tile (called `square` in the code). The domain of a tile is its different possible positions.
1. choose the tile on the grid whose domain is the smallest,
1. choose a position for the tile that is compatible with the adjacent tiles,
    - If more than one position of the tile are possible, add the others to the pile (and save the current state of the grid with them), then goto 2.
    - If no positions are compatible with the adjacent tiles, you are in a dead end. You have to explore another branch of the tree: pop an element from the pile and reset the grid with its data. Goto 2.
1. If the grid is full, you just found a solution! Now store it in a list and continue to explore the tree: unstack a new grid. Goto 2.
1. When the pile is empty, you explored the whole tree and found all the solutions - if there are solutions. Rejoice!

### Improvements
#### Forward Check

When you chose an orientation for a tile (let's call it T0), you can remove from the domains of the adjacent tiles (for instance T1) the orientations that are not compatible with the tile you just set. This is a forward check.

#### Arc-Consistency

When you restrict the domains of T1 with the forward check, the tiles adjacent to T1 (let's call it T2) can also include orientation that are not compatible anymore with the domain of T1, hence you can update T2's domain. And you can also recursively update the domain of the adjacent tiles of T2. This is arc-consistency.

## Results

#### Time to find all the solutions of the examples grids (without GUI) **in ms**:

| examples | number of solutions | dimensions |basic exploration|with forward check|with arc-consistency|
|----------|---------------------|------------|-----------------|------------------|--------------------|
| 0        |          0          |     3x3    |        2    ms  |         2    ms  |        3     ms    |
| 1        |          1          |     3x3    |        2    ms  |         3    ms  |        2     ms    |
| 2        |          1          |     5x5    |        18   ms  |        27    ms  |        22    ms    |
| 3        |          8          |     5x5    |        20   ms  |        35    ms  |        36    ms    |
| 4        |          2          |     7x9    |        60   ms  |      500  ms (!) |        75    ms    |
| gift     |          1          |    19x20   |      7 750  ms  |  several minutes |      12 600  ms    |

### Comments

*Simplicty is better when you implement yourself a problem specific solver*: the reason why the solver is slower with arc-consistency and forward-check is probably because the overhead of my code is too important and erases the possibles advantages brought by the "celverness" of the algorithms. The results are probably very different with an optimized and well coded solver.

However it is clear that forward check is rather useless for this problem as it only check the adjacent tiles and hence is not able to greatly reduce the exploration tree. If you want to check something in advance, you should check everything (ie maintain the arc consistency).

## Code organization

- The main part of the program is in `solver.py`,
- `misc.py` contains the input parsing code, the examples, the output printing code,
- `GUI.py`'s name is self-explanatory.



========================================

## Misc
The shapes are : ![shapes](tuiles.svg)

Link to the [TP](http://www-desir.lip6.fr/~durrc/Iut/optim/t/dm1-connect).


