
# Musical Parsing with the help of a Context-Free Grammar


## Principle

The goal of all this is to help analyse music by parsing pieces with the help of a context-free grammar, such as [this one](https://docdrop.org/download_annotation_doc/Rohrmeier---2020---The-Syntax-of-Jazz-Harmony-Diatonic-Tonal-b6eoz.pdf)  (by [Martin Rohrmeier](https://people.epfl.ch/martin.rohrmeier?lang=en))

## Remarks

- The implemeted algorithm is described in the pdf file given, and is aplicable to any context-free grammar in Chomsky normal form.
- The applicability to a grammar with additional rules of the type **A -> B**, where A and B are non-terminal elements, is discussed in the pdf (hopefully).
-  The chord are represented by (root pitch, quality).
Thus V/IV and I, for example, are represented the same.  
Inversions and key changes are not taken into account either.
- The algorithm tries to put a fixed number of chords per measure. This number is not modifiable inside of an analysis, which could cause problems as the 'chord rythm' of a piece is not constant in general.  
The rule **X -> X X** is covering this in most cases, but it could easily lead to some issues.

See USAGE.md for more informations specific to the current state of the code.

## Dependencies

- [UV](https://astral.sh/uv/) as a project/version manager
- [ms3](https://github.com/johentsch/ms3) to parse musical files
- [numpy](https://numpy.org/) and [pandas](https://pandas.pydata.org/docs/#) to handle tabloids










# DISOPT-Music-Parsing
