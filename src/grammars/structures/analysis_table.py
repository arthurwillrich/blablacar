import copy

#from src.automata.structures.state import State
from prettytable import PrettyTable
#from src.grammars.persistency.reader import read_grammar_from
from src.grammars.persistency.reader import read_grammar_from, new_read_grammar_from
from src.grammars.structures.cfg import ContextFreeGrammar

class AnalysisTableContrcutor:

    def __init__(self, grammar: ContextFreeGrammar):
        self.grammar = grammar
        self.productions = grammar.productions
        self.terminals = grammar.terminals
        self.start_state = grammar.start
        self.non_terminals = grammar.non_terminals
        self.split_productions = set()
        self.table = ''
        #self.split_productions = dict()

    def set_to_list(self, i: int):

        my_list = dict()


        if i == 1:
            for key, value in self.grammar.find_firsts().items():
                my_list[key] = list(value)
        if i == 2:
            for key, value in self.grammar.find_follows().items():
                my_list[key] = list(value)
        if i == 3:
            for key, value in self.grammar.productions.items():
                my_list[key] = list(value)
        return my_list

    def generate_table(self):

        first = self.set_to_list(1)
        follows = self.set_to_list(2)
        productions = self.set_to_list(3)

        non_terminals = list(self.non_terminals)
        terminals = (list(self.terminals) + ['$'])
        # terminals.remove(('&'))
        table = {nt: {t: str() for t in terminals} for nt in non_terminals}
        for nt in non_terminals:
            table[nt].pop('&', None)



        i = 1

        split_productions = dict()
        aux_dict = dict()
        self.terminals.add('$')


        for p in self.productions:
            for c in range(len(self.productions[p])):
                split_productions[i] = ((productions[p])[c-1])
                aux_dict[i] = p
                i = i+1
        print(split_productions)
        self.split_productions = split_productions


        #for key,value in first.items():
            #print(type(value))


        for non_terminal in self.non_terminals:
            firsts = first[non_terminal]

            for derivation in split_productions:
                # print(derivation)
                # print((split_productions[derivation])[0])
                if (split_productions[derivation])[0] in self.terminals:

                    if '&' in (split_productions[derivation])[0]:
                        split_productions[derivation][0] = '$'

                    if table[non_terminal][(split_productions[derivation])[0]] == '' and aux_dict[derivation] == non_terminal:
                        # print(type(split_productions[derivation]))
                        if split_productions[derivation][0] == '$':
                            for follow in follows[non_terminal]:
                                table[non_terminal][follow] = derivation
                            table[non_terminal][('$')[0]] = derivation

                        elif '$' in (split_productions[derivation])[0]:
                            (split_productions[derivation])[0] = '$'
                            table[non_terminal][(split_productions[derivation])[0]] = derivation

                        else:

                            table[non_terminal][(split_productions[derivation])[0]] = derivation
                else:
                    for key in firsts:
                        if key == '&':
                            key = '$'
                        if table[non_terminal][key] == '' and aux_dict[derivation] == non_terminal:
                            table[non_terminal][key] = derivation

        self.table = table

    def run_analysis(self, sentence):
        stacktrace = []
        stack = ['$']
        stack.append(self.start_state)
        entry = sentence + '$'
        accepted = False

        variables = self.non_terminals

        self.clean_entries()

        while entry != '' and stack != '':
            history = {"stack": stack, "entry": entry}
            stacktrace.append(copy.deepcopy(history))
            print(history)
            symbol = stack.pop()

            if symbol in variables:
                if symbol in self.table and entry[0] in self.table[symbol]:
                    derivation = self.table[symbol][entry[0]]
                    if derivation == '':
                        accepted = False
                        break


                    derivation = list(self.split_productions[derivation])
                    # for i in range (len(derivation)):
                    #     aux = derivation[i]
                    #     derivation.remove(derivation[i])
                    #     derivation.append(list(aux))

                    derivation = list(derivation[0])
                    derivation.reverse()

                    if derivation[0] == "$":
                        continue
                    stack += derivation
                else:
                    accepted = False
                    break
            elif symbol == entry[0]:
                if symbol == "$":
                    accepted = True
                    break
                else:
                    entry = entry[1:]
            else:
                accepted = False
                break
        print("Aceitou?: ", accepted)
        return stacktrace, accepted

    def clean_entries(self):
        for i in self.split_productions:
            result = []
            for der in self.split_productions[i]:
                if der not in result:
                    notresult = der
                    result.append(der)
            if len(result) > 1 :
                result.remove(notresult)
            self.split_productions[i] = result
# analysisTable = AnalysisTableContrcutor()
# analysisTable.read()
#
#
# table = PrettyTable()
#
# header = ['NonTerminal']
# for terminal in analysisTable.terminals:
#     header.append(terminal)
# header.append('$')
#
# table.field_names = header
#
# analysisTable.generate_table()
# analysisTable.run_analysis('ivi^i')

#for column in analysisTable.table:
   # lista = []
    #for line in analysisTable.table[column]:
       # print("teste: " ,(analysisTable.table[column])[line])

    #print((analysisTable.table[column])['i'])


if __name__ == '__main__':
    read_grammar = new_read_grammar_from('gramaticaexemplo.txt')
    analysisTable = AnalysisTableContrcutor(read_grammar)
    analysisTable.generate_table()
    analysisTable.run_analysis("ivi^i")

    table = PrettyTable()

    header = ['NonTerminal']
    for terminal in analysisTable.terminals:
        if terminal != '&':
            header.append(terminal)

    table.field_names = header

    for nt in analysisTable.non_terminals:
        entry = []
        entry.append(nt)
        mydict = analysisTable.table[nt]
        for t in analysisTable.terminals:
            if t != '&':
                entry.append(mydict[t])
        table.add_row(entry)

    print(table)




