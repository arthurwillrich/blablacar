from src import resource_dir
from src.grammars.structures.cfg import ContextFreeGrammar


def new_read_grammar_from(filepath) -> ContextFreeGrammar:
    with open(resource_dir / filepath, 'r') as f:
        lines = f.readlines()
        trimmed = [line.rstrip() for line in lines]

        nt_set = set()
        t_set = set()
        p_set = set()
        start = ""

        end_product = []
        for productions in trimmed:
            split_productions = productions.split("->")
            end_product.append(split_productions[1].strip())
            nt_set.add(split_productions[0].strip())
            if start == "":
                start = split_productions[0].strip()

        for product in end_product:
            aux = product.split("|")
            for a in aux:
                for char in list(a):
                    if char not in nt_set and char != "'" and char != " ":
                        t_set.add(char)
        p_set = __digest_productions_from(trimmed)

        return ContextFreeGrammar(nt_set, t_set, p_set, start)

def read_grammar_from(filepath) -> ContextFreeGrammar:
    with open(resource_dir / filepath, 'r') as f:
        lines = f.readlines()

    trimmed = [line.rstrip() for line in lines]

    start = __start_symbol_from(trimmed)
    non_terminals = __non_terminals_from(trimmed)
    terminals = __terminals_from(trimmed)
    productions = __digest_productions_from(trimmed)

    print(productions)

    return ContextFreeGrammar(non_terminals, terminals, productions, start)


def __start_symbol_from(lines):
    return lines[lines.index('#start') + 1]


def __non_terminals_from(lines):
    return {symbol for symbol in lines[lines.index('#non-terminals') + 1: lines.index('#terminals')]}


def __terminals_from(lines):
    return {symbol for symbol in lines[lines.index('#terminals') + 1: lines.index('#productions')]}


def __digest_productions_from(lines):
    productions = dict()

    for production in lines:
        line_without_arrow = production.split('->')
        non_terminal = line_without_arrow[0].replace(' ', '')  # Expected to always be non-terminal.
        digested_line = __eat(''.join(line_without_arrow[1:]).split('|'))
        productions[non_terminal] = digested_line

    return productions


def __eat(line: list):
    digest_line = list()

    for place in line:
        digest_line.append(place.split())

    return digest_line


def __show_first_from(cfg):
    for key, value in cfg.first().items():
        if key.isupper():
            print(key, value)
    print()


if __name__ == '__main__':
    grammar1 = read_grammar_from('reduced_grammar1.txt')
    print(grammar1.productions)
    __show_first_from(grammar1)
