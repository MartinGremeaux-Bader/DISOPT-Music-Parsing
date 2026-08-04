import numpy as np
import pandas as pd
import re
from definitions import Chord, Terminal_elem


'''the goal of this file is to get from a tsv file the weight matrix of terminal elements'''

RHO : float = 1/4 # punishment value for a non in-bar chord

PRECISION = 4 # the fraction of a bar we try to fit a chord in, for example PRECISION = 4 -> 4 chords in a bar


def note_to_pitch(note : str) -> int :
    '''"C5" -> 0 
    \n "Eb3" -> 3 
    \n etc.'''
    pitch = re.fullmatch('[ABCDEFG][#b]?[0-9]', note)
    if pitch == None :
        raise ValueError('unknown note', note)
    p = 'C.D.EF.G.A.B'.index(note[0])
    if len(note) == 3 :
        if note[1] == '#' :
            p += 1
        if note[1] == 'b' :
            p -= 1
    return p

def str_to_float(fraction:str) -> float :
    ''' "a/b" -> a/b '''
    assert re.fullmatch('[0-9]+(/[0-9]+)?', fraction)
    if not '/' in fraction :
        return float(fraction)
    slash = fraction.index('/')
    return float(fraction[:slash])/float(fraction[slash+1:])

def check_dura(start1 : float, end1 : float, start2 : float, end2 : float) -> bool :
    ''' Check if to 'time windows' (intervalls) overlap. A one-point overlap is not considered as an overlap.'''
    return (start1 <= start2 and start2 < end1) or (start2 <= start1 and start1 < end2)


def compare_notes(chord  : set[int], bar : list[int], punish : float = RHO, key = 0) -> float :
        ''' A totally arbitrary quantification of how well a chord fit in a bar
        \n use key to choose the comparaison mode :
        \n 0 -> only subset checking, 1 -> 'ponderate subset checking', other -> same as 1'''
        set_bar = set(bar)
        match key :
            case 0 :
                return chord.issubset(set_bar)
            case 1 :
                if not chord.issubset(set_bar) :
                    return punish * sum(  [ int(note in bar) for note in chord]   ) / len(chord)
                    # if not all notes of the chord in the piece : return punishment times "how much the chord is in the piece"
                else :
                    return sum([ (note in chord)  for note in bar ]) / len(bar)
                    # if the chord is in the piece : return "how much coes the chord cover the piece"
            case _ : # here we just do the same as in 1 mode to avoid unnecessary errors
                if not chord.issubset(set_bar) :
                    return punish * sum(  [ int(note in bar) for note in chord]   ) / len(chord)
                else :
                    return sum([ (note in chord)  for note in bar ]) / len(bar)





def create_Matrix(file : str, precision : int = PRECISION, punish : float = RHO, key = 0) :
    """create the weights matrix of terminal rules from a tsv file of the notes \n
    same formalism as in the ms3 module \n
    the key is for the mode of local ranking of chords, see compare_notes for more \n
    file is the relative path of the tsv file, I think"""

    # extract the notes as a panda DataFrame
    notes = pd.read_csv(file, sep='\t')

    # only keep interestngs properties    (and keep only a certain part of the pece if wanted)
    notes =notes.loc[notes.index[:271],["mc", "quarterbeats", "duration_qb", 'name']]

    # add the pitch as int
    notes.insert(len(notes.columns), "value", [note_to_pitch(notes.at[i, 'name']) for i in notes.index])

    # add the start & end of each notes (in quarter beats) as float 
    notes.insert(2, "qb", [str_to_float(notes.at[i, 'quarterbeats']) for i in notes.index])
    notes.insert(2, "end_qb", [notes.at[i, 'qb'] + notes.at[i, 'duration_qb'] for i in notes.index])

    # only keep interesting columns
    notes =notes.loc[notes.index,["mc", "qb", "end_qb", 'value']]
                   

    #print(notes.loc[notes.index[240:],notes.keys()])
    n : int = notes.at[len(notes.index)-1, 'mc']
    #print(n)

    '''
    #This is a example of what is possible to add some notes at the end to close earlier, if you want
    #Note that you will need to tweak the number of keys of measures a little bit by hand 
        s = pd.DataFrame([[5, 32, 31, 0]], columns = ["mc", "qb", "end_qb", 'value'])
        notes = pd.concat([notes, s], ignore_index = True)
        notes = pd.concat([notes, s], ignore_index = True) # just here to provide a closure on fifth bar for the tests
        s.at[s.index[0], 'value'] = 4
        notes = pd.concat([notes, s], ignore_index = True)
        s.at[s.index[0], 'value'] = 7
        notes = pd.concat([notes, s], ignore_index = True)
    '''

    measures : dict[int, list[int]] = dict()
    # dict that associate a 'measure' number (or a quarter measure if PRECISiON = 4, but anway a 'unit of time-window')
    # to the list of the pitches of the notes present in it.
    # Counts duplicata for the compare_notes function

    # computation of 'measures'
    for i in range(precision*n) :
        measures[i] = list()
        for j in notes.index :
            if check_dura(i, (i+1), PRECISION/4*notes.at[j, 'qb'], PRECISION/4*notes.at[j, 'end_qb']) :
                (measures[i]).append(notes.at[j, 'value'])



    #print(measures)


    Matrix = np.full((precision*n, len(Terminal_elem)), 0.0)
    # The famous initial weight matrix

    # the computation of the matrix, with compare_notes on each pair (chord, bar)
    for k in range(precision*n) :
        bar_notes = measures[k]
        for l, chord in enumerate(Terminal_elem) :
            assert (type(chord) == Chord)
            chord_notes = chord.notes()
            Matrix [k][l] = compare_notes(chord_notes, bar_notes, punish, key)
        
    return Matrix

#Matrix = create_Matrix('adapted cyk/K279-1.notes.tsv')
#print(Matrix)


def ind_max(lis : list) -> int :
    """return the index of the maximal element
    \n not efficient, only a test function to compare the efficiency of the algorithm with the 'naive' approach"""
    m = max(lis)
    for j, elem in enumerate(lis) :
        if elem == m :
            return j
    raise ValueError

def naive(Matrix) :
    '''the output of the naive algorithm, not taking the grammar in account
    \n only to compare, a priori'''
    l = []
    for i in range(Matrix.shape[0]) :
        l.append(ind_max(Matrix[i]))
    return l


















