from src.grammars.persistency.reader import new_read_grammar_from
from src.grammars.structures.analysis_table import AnalysisTableContrcutor
from src.grammars.structures.analysis_table import produce_pretty_table
import os
from os.path import dirname

if __name__ == '__main__':

    path = dirname(__file__)+'/'
    file = 'entry.txt'
    dir_list = os.listdir(path)
    print("List of directories and files before creation:")
    print(dir_list)
    print()

    with open(os.path.join(path, file), 'w') as fp:
        pass

    input("Digite a gramática em entry.txt e aperte enter")

    read_grammar = new_read_grammar_from(path+"entry.txt")

    print(read_grammar)



    # read_grammar = new_read_grammar_from('gramaticaexemplo.txt')
    # analysisTable = AnalysisTableContrcutor(read_grammar)
    # produce_pretty_table(analysisTable, "ivi^i") # arg1 : AnalysisTableContructor arg2 : entry to test

