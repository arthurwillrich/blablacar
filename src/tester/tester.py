from src.grammars.persistency.reader import new_read_grammar_from
from src.grammars.structures.analysis_table import AnalysisTableContrcutor
from src.grammars.structures.analysis_table import produce_pretty_table

if __name__ == '__main__':
    read_grammar = new_read_grammar_from('gramaticaexemplo.txt')
    analysisTable = AnalysisTableContrcutor(read_grammar)
    produce_pretty_table(analysisTable, "ivi^i") # arg1 : AnalysisTableContructor arg2 : entry to test

