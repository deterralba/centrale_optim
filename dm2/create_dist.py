from math import radians, cos, sin, asin, sqrt
from itertools import chain

def haversine(coord, to_coord):
    lat1, lon1, lat2, lon2 = map(radians, chain(coord, to_coord))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6373
    return c * r

vertexes = {}   # id -> (long, lat)
edges = {}      # vertexes -> list of vertexes
v125 = []       # list of 125 vertexes with >= 4 outgoing roads

with open('man.txt', 'rt') as f:
    for line in f:
        if line[0] == 'a':
            v1, v2, time = [int(nb) for nb in line.split()[1:]]
            l = edges.get(v1, [])
            edges[v1] = l + [v2]
        elif line[0] == 'v':
            id_, lat, long = line.split()[1:]
            vertexes[int(id_)] = (float(lat), float(long))
        else:
            raise ValueError(line)

v125 = [k for k, v in edges.items() if len(v)>= 4]

#print(vertexes)
#print(v125)
#print(len(v125))

if True:
    with open('man_dist.txt', 'wt') as f:
        for v in v125:
            coord = vertexes[v]
            for v_to, v_coord in vertexes.items():
                dist = haversine(coord, v_coord)
                #print(v, coord,  v_to, v_coord, dist)
                f.write('{} {} {}\n'.format(v, v_to, dist))

if True:
    with open('man_125.txt', 'wt') as f:
        f.write('\n'.join([str(v) for v in v125]))
