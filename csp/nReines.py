#!/usr/bin/env python3

from CentraleSupelec import CSP
import sys

n = int(sys.argv[1])
N = range(n)
P = CSP([set(range(n)) for x in N])
for y in N:
    for x in range(y):
        P.addConstraint(x, y, {(u, v) for u in N for v in N if u - v not in [x-y, 0, y-x]})
# P.maintain_arc_consistency()

count = 0
for sol in P.solve():
    count += 1
    if count == 1:
        if n < 20:   # sinon la grille est trop grande
            for i in N:
                for j in N:
                    if sol[i] == j:
                        print("# ", end='')
                    else:
                        print(". ", end='')
                print()
        else:
            print(sol)
    else:
        break

print("Nodes explored : %i " % P.nodes)
if count == 0:
    print("There is no solution")
elif count == 1:
    print("The solution is unique")
else:
    print("The solution is not unique")
