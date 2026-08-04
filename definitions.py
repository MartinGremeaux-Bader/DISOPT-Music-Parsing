import numpy as np

'''here we define the Chord class, which are objects with a (root) pitch attribute and a quality attribute
The attributes are not modifiable.
Note that the only accepted chord qualities are major, minor, dominant, half-diminished and full-diminished'''



class Chord():

    __pitch : int
    __quality : str

    def __init__(self, Pitch : int, Quality : str) :
        q = Quality.lower()
        if q not in {"maj", "min", "dom", "half-dim", "full-dim"} :
            raise ValueError("unknown chord quality : ", q)
        self.__pitch = Pitch%12
        self.__quality = q

    @property    
    def pitch(self):
        return self.__pitch
    @property    
    def quality(self):
        return self.__quality
    
    def __repr__(self) :
        return "(" + str(self.__pitch) + ", " + str(self.__quality) + ")"
    
    def notes(self) -> set[int] :
        ''' Returns the notes composing the chords, as a set of pitches. '''
        match self.__quality :
            case "maj" :
                return {self.__pitch, (self.__pitch + 4)%12, (self.__pitch + 7)%12}
            case "min" :
                return {self.__pitch, (self.__pitch + 3)%12, (self.__pitch + 7)%12}
            case "dom" :
                return {self.__pitch, (self.__pitch + 4)%12, (self.__pitch + 7)%12, (self.__pitch + 10)%12}
            case "half-dim" :
                return {self.__pitch, (self.__pitch + 3)%12, (self.__pitch + 6)%12, (self.__pitch + 10)%12}
            case "full-dim" :
                return {self.__pitch, (self.__pitch + 3)%12, (self.__pitch + 6)%12, (self.__pitch + 9)%12}
            case _ :
                raise ValueError("unknown chord quality : ", self.__quality)
        



# The table of al non-terminal chords which will be considered
non_terminal_elem = np.array([[Chord(pitch, quality) for quality in ["maj", "min"]] for pitch in range(12)])
assert(non_terminal_elem.shape == (12, 2))
# The starting element of the grammar, namely a (non-terminal) C major chord
Start = non_terminal_elem[0][0]

# The table of al terminal chords which will be considered
terminal_elem = np.array([[Chord(pitch, quality) for quality in ["maj", "min"]] for pitch in range(12)])


# The terminal/non-terminal elements, but in lists for better iteration during the algorithm
Non_terminal_elem = [non_terminal_elem[i][j] for i in range(non_terminal_elem.shape[0]) for j in range(non_terminal_elem.shape[1])]
Terminal_elem = [terminal_elem[i][j] for i in range(non_terminal_elem.shape[0]) for j in range(non_terminal_elem.shape[1])]



# the rules that creates terminal elements
terminal_rules : list[tuple[Chord, Chord]] = [(non_terminal_elem[i][j], terminal_elem[i][j]) for i in range(non_terminal_elem.shape[0]) for j in range(non_terminal_elem.shape[1])]

# the rules that does not create terminal elements. Initialised by hand in datas_setup, but declared here with the rest
rules : list[tuple[Chord, tuple[Chord, Chord]]] = []



# because at this point I kinda liked the minuscules for generation and Majuscules for final used thing,
# but for them it is the same
Terminal_rules = terminal_rules
Rules = rules