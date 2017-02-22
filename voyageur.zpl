set V := {1..14};
param long[V] := <1> 16.47, <2> 16.47, <3> 20.09, <4> 22.39, <5> 25.23, <6> 22.00, <7> 20.47, <8> 17.20, <9> 16.30, <10> 14.05, <11> 16.53, <12> 21.52, <13> 19.41, <14> 20.09;
param lat[V] := <1> 96.10, <2> 94.44, <3> 92.54, <4> 93.37, <5> 97.24, <6> 96.05, <7> 97.02, <8> 96.29, <9> 97.38, <10> 98.12, <11> 97.38, <12> 95.59, <13> 97.13, <14> 94.55;

var x[V cross V] binary;

minimize distance:
    sum <i> in V:
        sum <j> in V:
            sqrt((lat[i] - lat[j])**2 + (long[i] - long[j])**2) * x[i, j];

subto route_in:
    forall <i> in V:
        sum <j> in V:
            x[i, j] == 1;

subto route_out:
    forall <j> in V:
        sum <i> in V:
            x[i, j] == 1;


subto model1:
    forall U in powerset(V):
        sum <i> in U: sum <j> in V\U: x[i, j] >= 1;
#subto model1:
#    forall <U> in powerset(V) with card(U) >= 2 and card(U) <= card(V) - 2:
#        sum <i> in U: sum <j> in V\U: x[i, j] >= 1;

