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

        print("FIRSTS: ", first)
        print("FOLLOWS: ", follows)
        non_terminals = list(self.non_terminals)
        terminals = (list(self.terminals) + ['$'])
        # terminals.remove(('&'))
        table = {nt: {t: str() for t in terminals} for nt in non_terminals}
        for nt in non_terminals:
            table[nt].pop('&', None)



        i = 1

        split_productions = dict()
        aux_dict = dict()

        aux = new_read_grammar_from('prova.txt')
        self.productions = aux.productions


        self.terminals.add('$')


        for p in aux.productions:
            for c in range(len(aux.productions[p])):
                split_productions[i] = ((aux.productions[p])[c-1])
                aux_dict[i] = p
                i = i+1
        self.split_productions = split_productions

        for non_terminal in self.non_terminals:
            firsts = first[non_terminal]
            for derivation in split_productions:

                if (split_productions[derivation])[0][0] in self.terminals:

                    if split_productions[derivation][0] == '&':
                        split_productions[derivation][0] = '$'

                    if table[non_terminal][(split_productions[derivation])[0][0]] == '' and aux_dict[derivation] == non_terminal:

                        if split_productions[derivation][0] == '$':
                            for follow in follows[non_terminal]:
                                table[non_terminal][follow] = derivation

                            table[non_terminal][('$')[0]] = derivation


                        elif '$' in (split_productions[derivation])[0]:

                            (split_productions[derivation])[0] = '$'
                            table[non_terminal][(split_productions[derivation])[0][0]] = derivation
                        else:
                            table[non_terminal][(split_productions[derivation])[0][0]] = derivation

                elif (split_productions[derivation])[0][0] in self.non_terminals:

                    for key in first[(split_productions[derivation])[0][0]]:
                        if key == '&':
                            key = '$'
                        if table[non_terminal][key] == '' and aux_dict[derivation] == non_terminal:
                            table[non_terminal][key] = derivation
                    if self.is_nullable((split_productions[derivation])[0][0], firsts):
                        for follow in follows[(split_productions[derivation])[0][0]]:
                            if table[non_terminal][follow] == '' and aux_dict[derivation] == non_terminal:
                                table[non_terminal][follow] = derivation

        self.table = table

    def is_nullable(self, non_terminal, firsts):
        if '&' in firsts:
            return True
        else: return False


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

def produce_pretty_table(atc: AnalysisTableContrcutor, entrada: str):
    atc.generate_table()
    atc.run_analysis(entrada)

    table = PrettyTable()
    header = ['NonTerminal']
    for terminal in atc.terminals:
        if terminal != '&':
            header.append(terminal)

    table.field_names = header

    for nt in atc.non_terminals:
        entry = []
        entry.append(nt)
        mydict = atc.table[nt]
        for t in atc.terminals:
            if t != '&':
                entry.append(mydict[t])
        table.add_row(entry)

    print(table)




if __name__ == '__main__':
    read_grammar = new_read_grammar_from('grammar_test_table.txt')
    analysisTable = AnalysisTableContrcutor(read_grammar)
    produce_pretty_table(analysisTable, "ivi^i")



