import copy
import string


class ContextFreeGrammar:
    __MAX_FACTOR = 2
    __VARIABLES = set(string.ascii_uppercase)

    def __init__(self, non_terminals, terminals, productions: dict, start='S'):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.symbols: set = self.terminals | self.non_terminals
        self.productions = productions
        self.start = start
        self.number_state = dict()
        self.state_number = dict()

    def __str__(self):
        gatherer = str()
        for src, dst in self.productions.items():
            gatherer += '{} -> '.format(src)
            for i in dst:
                if i == dst[-1]:
                    gatherer += '{}'.format(' '.join(i))
                else:
                    gatherer += '{} | '.format(' '.join(i))
            gatherer += '\n'
        return gatherer

    def find_firsts(self):
        firsts = {symbol: set() for symbol in self.non_terminals}
        for i in range(10):
            for nt in self.non_terminals:
                for productions in self.productions[nt]:
                    for product in productions:
                        if product[0] in self.terminals:
                            tempset = set(firsts[nt])
                            tempset.add(product[0])
                            firsts[nt] = tempset
                        if product[0] in self.non_terminals:
                            counter = 0

                            for h in range(3):
                                if product[counter] in self.non_terminals:
                                    if self.isNullable(firsts[product[counter]]):
                                        counter += 1
                                        self.verify_first(counter, product, firsts, nt)

                            tempset = set(firsts[nt])
                            auxtempset = firsts[product[0]]
                            tempset = tempset | auxtempset
                            if '&' in tempset:
                                tempset.remove('&')
                            firsts[nt] = tempset

        return firsts

    def isNullable(self, my_list: set()):
        if '&' in my_list:
            return True
        else:
            return False

    def verify_first(self, i, product, firsts: set(), nt):

        if len(product) > i:
            if product[i] in self.terminals:
                tempset = firsts[nt]
                tempset.add(product[i])
                firsts[nt] = tempset
            if product[i] in self.non_terminals:
                tempset = firsts[nt]
                auxtempset = firsts[product[i]]
                tempset = tempset | auxtempset
                if '&' in tempset:
                    tempset.remove('&')
                firsts[nt] = tempset

    def find_follows(self):
        firsts = self.find_firsts()

        print("FIRSTS: ", firsts)

        follows = {non_terminal: set() for non_terminal in self.non_terminals}

        for loop in range(5):
            for nt in self.non_terminals:
                if nt == self.start:
                    follows[nt] = {'$'}
                for productions in self.productions[nt]:
                    for product in productions:
                        for i, _ in enumerate(product):
                            if product[i] in self.non_terminals and i < len(product) - 1:
                                if product[i + 1] in self.non_terminals:
                                    follows[product[i]] = firsts[product[i + 1]] | follows[product[i]]

                                    if '&' in follows[product[i]]:
                                        follows[product[i]].remove('&')
                                if product[i + 1] in self.terminals:
                                    follows[product[i]] = set(product[i + 1]) | follows[product[i]]
                                elif '&' in firsts[product[i]] and product[i + 1] in self.non_terminals:
                                    follows[product[i]] |= firsts[product[i + 1]]
                                    product_aux = [char for char in product]
                                    product_aux.remove(product[i])
                                    new = self.char_to_string(product_aux)
                                    productions.append(new)
                                    if '&' in follows[product[i]]:
                                        follows[product[i]].remove('&')
                                elif '&' in firsts[product[i]] and product[i + 1] in self.terminals:
                                    follows[product[i]] |= set(product[i])

                                    if '&' in follows[product[i]]:
                                        follows[product[i]].remove('&')
                                if product[i + 1] in self.non_terminals:
                                    if self.isNullable(firsts[product[i + 1]]):  # if self.nullable()[product[i+1]]:
                                        product_aux = [char for char in product]
                                        product_aux.remove(product[i + 1])
                                        new = self.char_to_string(product_aux)
                                        productions.append(new)

                            elif product[i] in self.non_terminals and i == len(product) - 1:
                                follows[product[i]] = follows[nt] | follows[product[i]]

        print("FOLLOWS: ", follows)
        return follows

    def char_to_string(self, a):
        new = ""
        for x in a:
            new += x
        return new

    def follow_helper(self, product, i):
        if len(product[i]) > i + 1:
            return product[i + 1]
        else:
            return ""

    # Python program to convert a list
    # of character

    def first(self):
        first = {symbol: set() for symbol in self.symbols}

        # Rules are different for terminals, as they are their own firsts.
        first |= {terminal: {terminal} for terminal in self.terminals}

        nullable = self.nullable()

        def build_for(symbol):
            productions = self.productions[symbol]

            for piece in productions:
                head = piece[0]

                if head in self.terminals or head == '&':  # Whether starts with a terminal or with &.
                    first[symbol] |= {head}
                else:  # Starts with a non-terminal.
                    for letter in piece:
                        if letter in self.non_terminals and not first[letter]:
                            build_for(letter)  # Executes a depth-first search from the given letter.

                        print(type(first[symbol]))
                        print(type(first[letter]))
                        first[symbol] |= first[letter]

                        if not nullable[symbol]:  # & will be added by default if found in other firsts,
                            first[symbol] -= {'&'}  # but it must not be added if the symbol is not itself nullable.
                            break

        # for non_terminal in self.non_terminals:
        for non_terminal in self.non_terminals:
            build_for(non_terminal)

        return first

    def nullable(self):
        """:returns: a (symbol, bool) dictionary built from the grammar.
        Terminals are not nullable by default. Non-terminals will
        be nullable if there is at least one path from which they can find an &."""
        nullable = {symbol: False for symbol in self.symbols}
        visited = {non_terminal: False for non_terminal in self.non_terminals}

        def check(symbol):
            productions = self.productions[symbol]

            for production in productions:
                if production == '&':
                    nullable[symbol] = True
                else:
                    for letter in production:
                        if letter in self.non_terminals and not visited[letter]:
                            visited[letter] = True
                            check(letter)

                    if all([nullable.get(letter) for letter in production]):
                        nullable[symbol] = True

        check(self.start)
        return nullable

    def follow(self):
        follow = {non_terminal: set() for non_terminal in self.non_terminals}
        first = self.first()

        for symbol in self.non_terminals:  # Gathers results from start until end.
            if symbol == self.start:
                follow[symbol] = {'$'}  # The start's follow() is fixed in $ by default.

            productions = self.productions[symbol]

            for production in productions:
                for letter in production:
                    if letter in self.non_terminals:
                        if letter == production[-1]:
                            follow[letter] |= follow[symbol]
                        else:
                            next_pos = production.index(letter) + 1
                            next_letters = production[next_pos:]

                            for next_letter in next_letters:
                                follow[letter] |= first[next_letter] - {'&'}

                                # As there are nullable non-terminals, they are passible of
                                # not happening. In such cases, the actual letter will
                                # receive its next letters follow()s until it find a non-nullable non-terminal.
                                if '&' not in first[next_letter]:
                                    break

        # As we checked every body in normal order, a last checking is needed
        # in order to identify which nullable productions will need its head's set of follow productions.
        nullable = self.nullable()
        for head, body in self.__reversed_nullable_productions().items():
            for piece in body:
                for letter in piece:
                    if letter in self.non_terminals:
                        next_pos = piece.index(letter) + 1
                        next_letter = piece[next_pos: next_pos + 1]

                        if next_letter not in self.terminals and next_letter != piece[-1]:
                            if nullable[letter] and next_letter:
                                if follow.get(next_letter):
                                    # If the actual letter is nullable, its next letter will receive its follow() set.
                                    follow[next_letter] |= follow[head]

        return follow

    def __reversed_nullable_productions(self):
        reversed_productions = {non_terminal: set() for non_terminal in self.non_terminals}

        for non_terminal in self.non_terminals:
            for production in self.productions[non_terminal]:
                if production[-1] in self.non_terminals:  # Checks if the productions ends with a non-terminal.
                    reversed_productions[non_terminal] |= {production[::-1]}

        return reversed_productions

    def prepair_recursion(self):
        products = self.productions
        dict_aux = dict()
        aux = 1
        for i in products:
            dict_aux[aux] = products[i]
            aux += 1

        return dict_aux

    def create_association(self):
        products = self.productions
        state_number = dict()
        number_state = dict()
        aux = 1
        for i in products:
            state_number[i] = aux
            number_state[aux] = i
            aux += 1
        self.state_number = state_number
        self.number_state = number_state
        return state_number

    def recursion(self):
        productions = self.prepair_recursion()
        assoc = self.create_association()

        # x = 1
        # y = 1
        #
        # continue_rescursion = True

        # while continue_rescursion:
        #     self.direct_recursion(productions[x], assoc, x)
        #     for i in productions:
        #         self.indirect_recursion(productions[i], assoc, i)


        for i in productions:
            print("PASSANDO : ", productions[i])
            self.indirect_recursion(productions[i], assoc, i)
        productions[i] = [x for x in productions[i] if x]
        print("MEIO: ", productions)
        for i in productions:
            print("PASSANDO : ", productions[i])
            self.direct_recursion(productions[i], assoc, i)

        print("FIM:", self.productions)

    def indirect_recursion(self, product, assoc, key):

        productions = product[:]

        print(productions)

        for product in productions:
            if product[0][0] in self.non_terminals:
                print(assoc)
                print(key)
                if assoc[product[0][0]] < key:
                    to_change = []
                    after = product[0][1:]
                    # product.remove(product[0])
                    for prod in self.productions[product[0][0]]:
                        to_change.append(prod[0] + after)
                    product.remove(product[0])
                    for aux in to_change:
                        self.productions[self.number_state[key]].append([aux])
                    self.productions[self.number_state[key]] = [x for x in self.productions[self.number_state[key]] if x]

    def direct_recursion(self, product, assoc, key):

        non_terminals = set(self.non_terminals)
        for nt in assoc:
            need_change = False
            productions = product[:]
            print("PRODUCTIONS:" , productions)
            to_remove = []
            product_aux = product[:]
            for i in range(len(productions)):
                if ((productions[i])[0])[0] in assoc:
                    if assoc[((productions[i])[0])[0]] <= key:
                        if assoc[product[i][0][0]] >= key:
                            to_remove.append(productions[i])
                            need_change = True
            for i in range(len(productions)):
                if (productions[i]) in to_remove:
                    product_aux.remove(productions[i][:])

            if need_change:
                new_nt = self.get_new_state()

                if assoc[nt] >= key:
                    for i in self.productions[nt]:
                        i[0] += new_nt

                    new_product = []
                    for i in to_remove:

                        if [i[0]] in self.productions[nt]:
                            self.productions[nt].remove([i[0]])
                        i[0] = i[0][1:]

                        new_product.append(i)

                        # print(nt)
                        # product_aux.remove(i)
                    new_product.append(['&'])
                    # print("ANTES> ", self.productions[new_nt])
                    self.productions[new_nt] = new_product

    def number_of_keys(self, dict):

        count = 0

        for key, value in dict.items():
            count += 1

        return count

    def get_new_state(self):
        disp = self.__VARIABLES - self.non_terminals
        return min(disp)

    def left_recursion(self):
        return self.eliminate_indirect_recursion()

    def eliminate_direct_recursion(self, non_terminal):
        contem = list()
        nao_contem = list()
        new_state = self.get_new_state()
        for production in self.productions[non_terminal]:
            head = production[0]
            tail = production[1:]
            if head == non_terminal:
                if len(tail) != 0:
                    contem.append(str().join(tail) + new_state)
                else:
                    continue
            else:
                nao_contem.append(str().join(production) + new_state)

        if len(contem) != 0:
            contem.append('&')
            self.non_terminals |= {new_state}
            self.productions[new_state] = contem

            if len(nao_contem) != 0:
                self.productions[non_terminal] = nao_contem
            else:
                nao_contem.append(new_state)
                self.productions[non_terminal] = nao_contem

    def eliminate_indirect_recursion(self):
        non_terminals = list(self.non_terminals)
        i = 0
        stop_condition = True
        new_productions = list()
        prod_to_remove = str()

        while stop_condition:
            for j in range(i):
                for production in list(self.productions[non_terminals[i]]):
                    head = production[0]
                    tail = production[1:]
                    print("H", head)
                    print("T", tail)
                    if head == non_terminals[j]:
                        new_productions.clear()
                        new_production = tail
                        for prod_ind in list(self.productions[non_terminals[j]]):
                            new_productions.append(prod_ind + new_production)
                        prod_to_remove = production

                for new_prod in list(new_productions):
                    self.productions[non_terminals[i]].append(new_prod)
                if prod_to_remove and prod_to_remove in self.productions[non_terminals[i]]:
                    print("PDR:", prod_to_remove)
                    self.productions[non_terminals[i]].remove(prod_to_remove)

            self.eliminate_direct_recursion(non_terminals[i])
            i = i + 1
            if i >= len(non_terminals):
                stop_condition = False

        print("NT: ", self.non_terminals)
        print("T: ", self.terminals)
        print("P: ", self.productions)
        print("S: ", self.start)

        return ContextFreeGrammar(self.non_terminals, self.terminals, self.productions, self.start)

    def number_derivation(self):
        productions_non_terminals = list()
        for prod in self.productions:
            productions_non_terminals.append(prod[0])
        productions_non_terminals = list(dict.fromkeys(productions_non_terminals))
        return len(productions_non_terminals)

    def factor(self):
        # self.left_recursion()
        iterations = 0
        while iterations < ContextFreeGrammar.__MAX_FACTOR:
            # length = self.number_derivation()
            # for _ in range(1):
            self.eliminate_direct_non_determinism()
            self.eliminate_indirect_non_determinism()
            iterations += 1

    def eliminate_direct_non_determinism(self):
        variables = list(self.non_terminals)
        for variable in variables:
            derivations = list(self.productions[variable])
            derivation_to_change = {}
            print(derivations)
            # print(derivation_to_change)
            for derivation in derivations:
                head = derivation[0]
                tail = derivation[1:]
                if head not in derivation_to_change:
                    derivation_to_change[head] = []
                derivation_to_change[head].append(tail)
                print(derivation_to_change)

            for head, tails in derivation_to_change.items():
                already_added = False
                if len(tails) == 1:
                    print("entrou")
                    continue
                else:
                    print("entrou")
                    productions_new_state = list()
                    new_state = self.get_new_state()
                    self.non_terminals |= {new_state}
                    self.productions[new_state] = {}
                    for tail in tails:
                        if tail == '':
                            productions_new_state.append('&')
                        else:
                            productions_new_state.append(tail)
                        if not already_added:
                            self.productions[variable].append(head + new_state)
                            already_added = True
                        self.productions[variable].remove(head + tail)

                    resultant_list = []
                    for element in productions_new_state:
                        if element not in resultant_list:
                            resultant_list.append(element)

                    # print("Oi")
                    self.productions[new_state] = resultant_list

    def remove_indirect_non_determinism(self):
        variables = self.get_variables()
        for variable in variables:
            derivations = copy.deepcopy(self.dictionary[variable])
            for derivation in derivations:
                head, *tail = derivation
                tail = "&" if len(tail) == 0 else "".join(tail)
                if self.__is_variable(head):
                    self.dictionary[variable].remove(derivation)
                    for subderivation in self.dictionary[head]:
                        if subderivation == "&":
                            new_derivation = tail
                        elif tail == "&":
                            new_derivation = subderivation
                        else:
                            new_derivation = subderivation + tail
                        if new_derivation not in self.dictionary[variable]:
                            self.dictionary[variable].append(new_derivation)

    def __is_variable(self, character):
        return character.isupper()
