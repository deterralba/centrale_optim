# Import data from files
param graphfile := "man.txt";
param distfile := "man_dist.txt";
param file125 := "man_125.txt";
set V := { read graphfile as "<2n>" comment "a"};
set E := { read graphfile as "<2n,3n>" comment "v"};
set P := { read file125 as "<1n>"};
param dist[P cross V] := read distfile as "<1n,2n> 3n";

param b1 := 283492455;
param b2 := 283494345;
var open[P] >=0 <=1;  # 1 if post is open, else 0
var client[V cross P] >=0 <=1;  # 1 if post P is the closest from V


minimize nb_open_post:
    (sum <p> in P: 500*open[p]) + (sum <v,p> in V cross P: client[v,p]*dist[p,v]);

subto open_posts: open[b1] == 1 and open[b2] == 1;

subto unique_post_per_client:
    forall <v> in V do
        sum <p> in P: client[v,p] == 1;

subto client_can_go_only_if_post_open:
    forall <v,p> in V cross P do
         client[v,p] <= open[p];

