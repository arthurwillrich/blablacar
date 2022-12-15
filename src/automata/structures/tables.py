from prettytable import PrettyTable
from src.automata.persistency.reader import read_fa_from

#Tabela de simbolos - Tem que arrumar

class Env:

    def __init__(self):
        self.st = {}
        self.tl = []
        # self.prev = p

    def putST(self, s: str, st):
        if s not in self.st:
            self.st[s] = len(self.st)
            st.add_row([len(self.st),s])
        return self.st.get(s)

    def putTL(self, s, tl):
        if s not in self.tl:
           tl.add_row([s])
           self.tl.append(s)

if __name__ == '__main__':
    rw_file = open('reserved_words.txt', 'r')
    rw_read = rw_file.readlines()
    reservedTerms = []
    entry = []
    for line in rw_read:
        reservedTerms.append(line[:-1])

    entry_file = open('entry_tabel.txt', 'r')

    for line in entry_file:
        for word in line.split():
            entry.append(word)

    tables = Env()

    st = PrettyTable()
    st.field_names = ["index", "id"]
    tl = PrettyTable()
    tl.field_names = ["Token List"]

    place = 0

    for word in entry:
        contains = False
        for terms in reservedTerms:
            reserved = terms.split()
            for words in reserved:
                if word in words:
                    contains = True
                    classes = reserved[0]
        if contains:
            tables.putTL([word, classes, place], tl)
            place += 1
        else:
            index = tables.putST(word)
            tables.putTL([word, "not reserved", index+1], tl)

    print(st)
    print(tl)