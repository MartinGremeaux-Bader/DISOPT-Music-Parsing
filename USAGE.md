# How to use


### What the files do :


- main : To call everything.

- algo : The algorithm is implemented here. Note that it is valid for any free-context grammar, provided that you change the type prerequisites.

- definitions : Define the class Chord and lists of chords that are used in every file.

- datas_setup : Where the grammar is constructed, and where you can change parameters like which weght function is used or which rule is in the grammar.
Hopefully for using this programm you will only need to modify this file.

- Starting_Matrix : Where the starting matrix in input of the algorithm is computed.
The computation parameters can be modified in datas_setup.

- tests : To do some tests. Not useful.


### Warnings & Remarks : 

 - The chord are represented by (root pitch, quality).
Thus V/IV and I, for example, are represented the same, inversions and key changes are not taken into account.

 - Currently only the major and minor chords are taken into account.
This is modifiable by changing 'non_terminal_elem' and 'terminal_elem' in definitions, just add the chord quality wanted in the list runned through by the 'quality' variable.

 - An interesting thing to do could be to less punish a chord that is not in the bar but whose root is.

 - An current problem of the algorithm is that it tries to fit x chords per bar on the entire piece, but the real x could change along it.

 - Starting_Matrix is designed to make it possible to only consider a part of the piece relatively easily, but you will have to modify the create_Matrix function in it.
Some commentaries indicate what could be done to this extent.
