from collections import namedtuple

edgeT = namedtuple('edgeT', 'vertexes')
vertexT = namedtuple('vertexT', 'id, neighbors, variables')

vertexes = [
    vertexT(0, [1, 4, 7], []),
    vertexT(1, [0, 2, 5], []),
    vertexT(2, [1, 3, 9], []),
    vertexT(3, [2, 4, 6], []),
    vertexT(4, [0, 3, 8], []),
    vertexT(5, [1, 6, 8], []),
    vertexT(6, [3, 5, 7], []),
    vertexT(7, [0, 6, 9], []),
    vertexT(8, [5, 4, 9], []),
    vertexT(9, [2, 7, 8], []),
]

def extract_vortex(vertexes, id):
    return [v for v in vertexes if v.id == id][0]

for v in vertexes:
    for i in range(1, 4):
        v.variables.append(v.id*3 + i)

# it is easier to directly input the edges rather than dedude them from the vertexes.. but what is done is done
edges = []
for v in vertexes:
    for neighbor in v.neighbors:
        l = sorted([v.id, neighbor])
        if l not in [e.vertexes for e in edges]:
            edges.append(edgeT(l))

to_v = list(range(10))
cons = []

for v in vertexes:
    # we need at least one color
    cons.append('{} {} {}'.format(*v.variables))

    for var in v.variables:
        # we only need one color
        l = [-i for i in v.variables if i != var]
        cons.append('{} {}'.format(*l))


for e in edges:
    n1 = extract_vortex(vertexes, e.vertexes[0])
    n2 = extract_vortex(vertexes, e.vertexes[1])
    for i in range(3):
        cons.append('{} {}'.format(*sorted([-n1.variables[i], -n2.variables[i]])))

print('p cnf {} {}'.format(30, len(cons)))
for c in cons:
    print(c, ' 0')

