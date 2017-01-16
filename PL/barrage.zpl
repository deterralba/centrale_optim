param graphfile := "man.txt";
param source := 283492455;
param target := 283494345;


set V := { read graphfile as "<2n>" comment "a"};
set A := { read graphfile as "<2n,3n>" comment "v"};
param time[A] := read graphfile as "<2n,3n> 4n" comment "v";

var x[A] >= 0 <= 1;
var f >= 0;

maximize flot: sum<source, u> in A: x[source,u];
#minimize cost: sum<u,v> in A: x[u,v]*time[u,v];

subto flow_conservation:
forall <v> in V - {source, target}:
    sum <u,v> in A: x[u,v] == sum <v,u> in A: x[v,u];

# something goes out of the source
subto single_path_leaving1:
    sum <source,u> in A: x[source,u] == f;

# nothing goes in of the source
subto single_path_arriving0:
    sum <v,source> in A: x[v,source] == 0;
