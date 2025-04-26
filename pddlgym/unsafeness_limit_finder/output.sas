begin_version
3
end_version
begin_metric
0
end_metric
12
begin_variable
var0
-1
2
Atom free(l-1-1)
NegatedAtom free(l-1-1)
end_variable
begin_variable
var1
-1
2
Atom free(l-1-3)
NegatedAtom free(l-1-3)
end_variable
begin_variable
var2
-1
2
Atom free(l-3-1)
NegatedAtom free(l-3-1)
end_variable
begin_variable
var3
-1
2
Atom free(l-3-3)
NegatedAtom free(l-3-3)
end_variable
begin_variable
var4
-1
2
Atom free(l-1-2)
NegatedAtom free(l-1-2)
end_variable
begin_variable
var5
-1
2
Atom free(l-2-1)
NegatedAtom free(l-2-1)
end_variable
begin_variable
var6
-1
2
Atom free(l-2-3)
NegatedAtom free(l-2-3)
end_variable
begin_variable
var7
-1
2
Atom free(l-3-2)
NegatedAtom free(l-3-2)
end_variable
begin_variable
var8
-1
2
Atom free(l-2-2)
NegatedAtom free(l-2-2)
end_variable
begin_variable
var9
-1
9
Atom at(a, l-1-1)
Atom at(a, l-1-2)
Atom at(a, l-1-3)
Atom at(a, l-2-1)
Atom at(a, l-2-2)
Atom at(a, l-2-3)
Atom at(a, l-3-1)
Atom at(a, l-3-2)
Atom at(a, l-3-3)
end_variable
begin_variable
var10
-1
2
Atom sampled(r1)
NegatedAtom sampled(r1)
end_variable
begin_variable
var11
-1
2
Atom unsafe-token0()
Atom unsafe-token1()
end_variable
0
begin_state
0
0
0
0
1
0
0
0
1
1
1
1
end_state
begin_goal
2
9 1
10 0
end_goal
25
begin_operator
move a l-1-1 l-1-2
0
4
0 9 0 1
0 0 -1 0
0 4 0 1
0 11 -1 1
1
end_operator
begin_operator
move a l-1-2 l-1-1
0
4
0 9 1 0
0 0 0 1
0 4 -1 0
0 11 -1 1
1
end_operator
begin_operator
move a l-1-2 l-1-3
0
4
0 9 1 2
0 4 -1 0
0 1 0 1
0 11 -1 1
1
end_operator
begin_operator
move a l-1-3 l-1-2
0
4
0 9 2 1
0 4 0 1
0 1 -1 0
0 11 -1 1
1
end_operator
begin_operator
move a l-2-1 l-1-1
0
4
0 9 3 0
0 0 0 1
0 5 -1 0
0 11 -1 1
1
end_operator
begin_operator
move a l-2-1 l-3-1
0
4
0 9 3 6
0 5 -1 0
0 2 0 1
0 11 -1 1
1
end_operator
begin_operator
move a l-2-2 l-1-2
0
4
0 9 4 1
0 4 0 1
0 8 -1 0
0 11 -1 1
1
end_operator
begin_operator
move a l-2-2 l-3-2
0
4
0 9 4 7
0 8 -1 0
0 7 0 1
0 11 -1 1
1
end_operator
begin_operator
move a l-2-3 l-1-3
0
4
0 9 5 2
0 1 0 1
0 6 -1 0
0 11 -1 1
1
end_operator
begin_operator
move a l-2-3 l-3-3
0
4
0 9 5 8
0 6 -1 0
0 3 0 1
0 11 -1 1
1
end_operator
begin_operator
move a l-3-1 l-3-2
0
4
0 9 6 7
0 2 -1 0
0 7 0 1
0 11 -1 1
1
end_operator
begin_operator
move a l-3-2 l-3-1
0
4
0 9 7 6
0 2 0 1
0 7 -1 0
0 11 -1 1
1
end_operator
begin_operator
move a l-3-2 l-3-3
0
4
0 9 7 8
0 7 -1 0
0 3 0 1
0 11 -1 1
1
end_operator
begin_operator
move a l-3-3 l-3-2
0
4
0 9 8 7
0 7 0 1
0 3 -1 0
0 11 -1 1
1
end_operator
begin_operator
sample a r1 l-3-2
1
9 7
2
0 10 -1 0
0 11 -1 1
1
end_operator
begin_operator
move-unsafe-copy-1 a l-1-1 l-2-1
0
4
0 0 -1 0
0 5 0 1
0 9 0 3
0 11 1 0
1
end_operator
begin_operator
move-unsafe-copy-1 a l-1-2 l-2-2
0
4
0 4 -1 0
0 8 0 1
0 9 1 4
0 11 1 0
1
end_operator
begin_operator
move-unsafe-copy-1 a l-1-3 l-2-3
0
4
0 1 -1 0
0 6 0 1
0 9 2 5
0 11 1 0
1
end_operator
begin_operator
move-unsafe-copy-1 a l-2-1 l-2-2
0
4
0 5 -1 0
0 8 0 1
0 9 3 4
0 11 1 0
1
end_operator
begin_operator
move-unsafe-copy-1 a l-2-2 l-2-1
0
4
0 5 0 1
0 8 -1 0
0 9 4 3
0 11 1 0
1
end_operator
begin_operator
move-unsafe-copy-1 a l-2-2 l-2-3
0
4
0 6 0 1
0 8 -1 0
0 9 4 5
0 11 1 0
1
end_operator
begin_operator
move-unsafe-copy-1 a l-2-3 l-2-2
0
4
0 6 -1 0
0 8 0 1
0 9 5 4
0 11 1 0
1
end_operator
begin_operator
move-unsafe-copy-1 a l-3-1 l-2-1
0
4
0 2 -1 0
0 5 0 1
0 9 6 3
0 11 1 0
1
end_operator
begin_operator
move-unsafe-copy-1 a l-3-2 l-2-2
0
4
0 7 -1 0
0 8 0 1
0 9 7 4
0 11 1 0
1
end_operator
begin_operator
move-unsafe-copy-1 a l-3-3 l-2-3
0
4
0 3 -1 0
0 6 0 1
0 9 8 5
0 11 1 0
1
end_operator
0
