param n := 20;

set N := { 0 .. n-1 };
set G := N cross N;

var x[G] binary;

minimize lexico: sum <r,c> in G: (c / (n ** r) )* x[r,c];

subto row_has_queen: forall <r> in N do
    sum<c> in N: x[r, c] == 1;

subto col_has_queen: forall <c> in N do
    sum<r> in N: x[r, c] == 1;

subto diagonal: forall <d> in {0 .. 2 * n - 2} do
    sum<r,c> in G with r + c == d: x[r,c] <= 1;

subto antidiagonal: forall <d> in {0 .. 2 * n - 2} do
    sum<r,c> in G with r - c == d - (n - 1): x[r,c] <= 1;
