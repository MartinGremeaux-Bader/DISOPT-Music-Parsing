import numpy as np
from definitions import Chord, non_terminal_elem, Start, Non_terminal_elem, Terminal_elem, rules, Terminal_rules, Rules # regroups all things that will be imported in algo
import Starting_matrix as Sm

"""this file is to choose the exacts parameters that will be used in the algoritm
here you can modify :
- the musical file to be parsed
- the weight function
- the different rules in the grammar and their costs
- the computation mode of the initial matrix
- the relative weight of the initial matrix (I think choosing it such that matrix entries have the same order from the rules' weights is reasonable)
- the precision of chord-fitting it tries to achieve
- the punishment to calculate the weight of a non-fitting chord (as a subset)
"""

# PARAMETERS

FILE = 'K279-1.notes.tsv'

INITIAL_WEIGHT = 20

PRECISION = 4 # the fraction of a bar we try to fit a chord in, for example PRECISION = 4 -> 4 chords in a bar

PUNISH = 1/4 # punishment value for a non in-bar chord (we multiply our value by PUNISH if the chord is not in the bar)

COMP_MODE = 1 # in {0, 1}, the computation mode of the initial weights matrix





weight : dict[  tuple[Chord, tuple[Chord, Chord]]|tuple[Chord, Chord],   float ] = dict()

# here the weight function is just picking the weight of the rule from a dict containing all weights we define along with the rules
# note that the weights are totally arbitrary
def Weight(rule, r_Weight = 0, l_Weight = 0):
    '''The weight function'''
    try :
        return weight[rule] + r_Weight + l_Weight
    except :
        raise ValueError("unknown/undefined rule")


# here we manually create all the rules in the grammar, X -> Y Z being represented as (X, (Y, Z))
# note that they are not rules generating terminal elements.
# The only rules doing so are the 'trivial ones', which associate a non-terminal chord to the exact same chord, but terminal. 
for i in range(non_terminal_elem.shape[0]) :
    for j in range(non_terminal_elem.shape[1]) :
        chord : Chord = non_terminal_elem[i][j]
        rule1 = (chord, (non_terminal_elem[(i+7)%12][0], chord)) # X -> V/X X
        weight[rule1] = 8
        rule2 = (chord, (non_terminal_elem[(i+7)%12][1], chord)) # X -> v/X X
        weight[rule2] = 3
        rule3 = (chord, (chord, chord)) # X -> X X
        weight[rule3] = 4
        rule4 = (chord, (non_terminal_elem[(i+5)%12][0], chord)) # X -> IV/X X
        weight[rule4] =4

        rules.append(rule3)
        rules.append(rule2)
        rules.append(rule1)
        rules.append(rule4)

#the starting matrix we get with theses parameters
P_Matrix = Sm.create_Matrix(FILE, PRECISION, PUNISH,  COMP_MODE)*INITIAL_WEIGHT




