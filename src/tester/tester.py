from src.automata.determinization.conversion import determinize
from src.grammars.persistency.reader import new_read_grammar_from
from src.grammars.structures.analysis_table import AnalysisTableContrcutor
from src.grammars.structures.analysis_table import produce_pretty_table
import os
from os.path import dirname
#import only system from os
from os import system, name

# import sleep to show output for some time period
from time import sleep
from src.regex.conversion import fa_from
from src.regex.tree import SyntaxTree, show_tree_from



    # now call function we defined above
if __name__ == '__main__':

    loop = True

    while(loop):

        parte = input("""Digite se quer testar: 
                      '1' - PARTE 1
                      'rec' - recursão
                      'fat' - fatoração
                      'tab' - gerar tabela
                      'anl' - analisar entrada 
                      'ffg' - calcular first e follows
                      
                      """)


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

        elif parte == 'rec':
            grammar1 = new_read_grammar_from('direct_rec.txt')
            print("========== GRAMATICA ============")
            print(grammar1)

            print("============= RECURSAO =============")
            grammar1.recursion()

            print()

        elif parte == 'fat':
            grammar1 = new_read_grammar_from('fatoracao.txt')
            print("========== GRAMATICA ============")
            print(grammar1)

            print("============= FATORACAO =============")
            grammar1.factor()

        elif parte == 'ffg':
            read_grammar = new_read_grammar_from('prova.txt')
            analysisTable = AnalysisTableContrcutor(read_grammar)


            produce_pretty_table(analysisTable, "cvfm;be;be")

        elif parte == 'fim':
            loop = False



    # read_grammar = new_read_grammar_from('gramaticaexemplo.txt')
    # analysisTable = AnalysisTableContrcutor(read_grammar)
    # produce_pretty_table(analysisTable, "ivi^i") # arg1 : AnalysisTableContructor arg2 : entry to test
