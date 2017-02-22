
# incomplet: voir correction en ligne

set MOIS := {1..12};
set MOIS_ARRET := {1..11}; # 2 mois consecutifs
set MACH := {1, 2};
param d[MOIS] := <1> 10200, <2> 13100, <3> 9500, <4> 11500, <5> 12000, <6> 13500, <7> 11500, <8> 8000, <9> 14500, <10> 16000, <11> 11500, <12> 10800;
param a[MACH] := <1> 450, <2> 380; # bouteilles par jours
param l[MACH] := <1> 9, <2> 5; # nb ouvrier par machine
param production_par_ouvrier[MACH] := <1> 45, <2> 76;
# nombre de jours ouvr'es par mois
param j[MOIS] := <1> 22, <2> 20, <3> 23, <4> 19, <5> 20, <6> 21, <7> 20, <8> 22, <9> 21, <10> 22, <11> 21, <12> 20;

var y[MOIS][MACH] >= 0; # MATRIX NB jour-homme machine k au mois i
var X[MOIS_ARRET][MACH] >= 0; # MACH arréter pdt les mois i et i+1 (X=1)
var avg = sum <mach> in MACH: sum <mois> in MOIS: y[mois, mach] / 12

minimize fluctuation:
    sum <mois> in MOIS:

# nb de jours homme par mois par machine <= nb de jours ouvres du mois * nb d ouvriers necessaires par machine
# ie pas de machine en sur production homme
subto nbre_ouvriers:
    forall i in {2..11}:
        forall k in MACH:
            y[i,k] <= l[k] * j[i] * (1 - (X[i,k] + X[i-1,k]));
    # meme chose mais pour le 1er mois
    forall k in MACH:
        y[1,k] <= l[k] * j[1] * (1 - X[1,k])
    # idem pour le dernier mois
    forall k in MACH:
        y[12,k] <= l[k] * j[12] * (1 - X[11,k])

subto demande_satisfaites:
    forall mois in MOIS:
        sum <mach> in MACH: sum <child_mois> in <MOIS> with child_mois <= mois:
            y[i,mach]*production_par_ouvrier[mach] >= sum <child_mois> in MOIS with mois <= mois: d[child_mois]

subto vacances:
    forall i in {7,8}:
        sum <mach> in MACH: X[i, mach] + X[i-1, mach] >= 1

