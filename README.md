# simple-parser
A simple recursive-descent parser for a simple expression language that I started as a proof of concept.  The code scanner uses a state machine that is maintained in 'statedef.py', the unique feature of which is that it uses a character classification to reduce the size of the state table. 

The parser itself uses basic techniques, much help from past endeavors as well as Rober Nysom's "Crafting Interpreters".

