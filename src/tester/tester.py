from src.automata.determinization.conversion import determinize
from src.grammars.persistency.reader import new_read_grammar_from
from src.grammars.structures.analysis_table import AnalysisTableContrcutor
from src.grammars.structures.analysis_table import produce_pretty_table
import os
from os.path import dirname

from src.regex.conversion import fa_from
from src.regex.tree import SyntaxTree, show_tree_from

if __name__ == '__main__':

    loop = True

    while(loop):

        parte = input("Digite se quer testar a parte 1 ou parte 2")


        if parte == '1':
            with open('entry.txt') as f:
                lines = f.readlines()
                er1 = lines[0][:-1]
                er2 = lines[1]


            print(er1)
            print(er2)


            fa1 = fa_from(er1)
            t1 = SyntaxTree(er1)
            show_tree_from(t1.root)
            print(fa1)

            print("===============================")

            fa2 = fa_from(er2)
            t2 = SyntaxTree(er2)
            show_tree_from(t2.root)
            print(fa2)


            print("+++++++++++++ UNIAO ++++++++++++++")
            print(fa1|fa2)
            uniao = (fa1|fa2)

            print("+++++++++++ DETERMINIZACAO ++++++++++++++++")
            uniao = determinize(uniao)
            print(uniao)

        elif parte == '2':
            grammar1 = new_read_grammar_from('direct_rec.txt')
            grammar1.factor()
            print(grammar1)
        elif parte == 'clear':
            pass
        elif parte == 'fim':
            loop = False



    # read_grammar = new_read_grammar_from('gramaticaexemplo.txt')
    # analysisTable = AnalysisTableContrcutor(read_grammar)
    # produce_pretty_table(analysisTable, "ivi^i") # arg1 : AnalysisTableContructor arg2 : entry to test

