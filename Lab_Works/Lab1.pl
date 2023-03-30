add(X,Y):- A is X+Y,
            write(A).

PREDICATES1
NONDETERM hcf(integer,integer,integer).

CLAUSES
hcf(X,Y,Z):-(Y mod X)=0,Z=X.
hcf(X,Y,Z):-(Y mod X)>0,Temp=(Y mod X),hcf(Temp,X,Z).

GOAL
hcf(17,23,Z).


PREDICATES2
NONDETERM move(integer,STRING,STRING,STRING)
CLAUSES
move(1,X,Y,Z) :-
   write("Move top disk from "), 
   write(X), 
   write(" to "), 
   write(Y),
   nl.
move(N,X,Y,Z) :-
   N>1,
   M = N-1,
   move(M,X,Z,Y),
   move(1,X,Y,Z),
   move(M,Z,Y,X).
GOAL
move(5,"Start","End","Auxilliary").


DOMAINS
list = integer*
PREDICATES
add(list,integer)
CLAUSES
add([H|T],SUM):-
	add(T,SUM1),
	SUM =H+SUM1.
add([],SUM):-
	SUM =0.
GOAL
add([5,3,5,9,3,11,2,15,18,10,16],Z).

DOMAINS
list = integer*
PREDICATES
append(list,list,list)
CLAUSES
append([H|T],L2,L3):-
	append(T,L2,L4),
	L3 =[H|L4].
append([],L2,L2).
GOAL
append([1,3,10],[3,4,5,6,7,8],X).

DOMAINS
list = integer*
PREDICATES
append(list,list,list)
CLAUSES
append([H|T],L2,L3):-
	append(T,L2,L4),
	L3 =[H|L4].
append([],L2,L2).
GOAL
append([1,3,10],[3,4,5,6,7,8],X).
 
 
 DOMAINS
list = integer*

PREDICATES
NONDETERM condition(integer)
NONDETERM display(list)
NONDETERM begin(list)

CLAUSES
condition(X):- 
	X=1;X=2.

begin(L):-
	write("["), 
	display(L).
	
display([H|T]):- 
	condition(H), 
	write(H), 
	write(","), 
	display(T).
display([H|T]):- 
	display(T).
display([]):-
	write("]"),
	readint(X).

GOAL
begin([1,2,4,5,2,4,5,1,1]).


