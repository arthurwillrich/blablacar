# blablacar
Trabalho para a disciplina de Linguagens Formais e Compiladores

## Primeiros passos

Para utilização do blablacar, é nescessária a versão do Python 3.10 ou superior e a biblioteca "PrettyTable"

1. `Python3.10`

`sudo apt update && sudo apt upgrade -y`\
`sudo apt install software-properties-common -y`\
`sudo add-apt-repository ppa:deadsnakes/ppa`\
`sudo apt install python3.10`

2. `PrettyTable`

Para instalar a `PrettyTable`, você precisa que a versão do`pip` seja compatível com `Python3.10`.

`sudo apt install python3.10-distutils`\
`python3.10 -m pip install -U prettytable`

## How does it work?

The code will, indeed, look a lot more like
a lib than an application. Due to the fact
there is no `main` module at the time
being, users may be confused at the beggining, thus
it is worth mentioning that every project module works
as a `main` in its own way.

There are 3 big topics from the field of
Formal Languages implemented here:

1. Finite Automata (FA);
2. Grammars;
3. Regular Expressions (regex).
    
### Finite Automata (FA)

There is no explicit distinction between those
that are deterministic and their counterpart.
Every FA will have:

    1. A set containing all of its states;
    2. An initial state;
    3. A set of all its final states; and
    4. A transition dictionary, indexed by
    tuples of (State, Symbol).

There is no need to keep the alphabet in a variable.
Its only usage in the project is at the process
of `determinization`, but, if one does need it,
there is `FiniteAutomata.symbols()` to retrieve
an alphabet from a FA.

The `FiniteAutomata` class overrides the `__or__()`
and the `__str__()` as the user is able to get
the union of 2 automata like this:

> `fa3 = fa1 | fa2`

To see the result, `PrettyTable` package helps us
to show the FA in user-friendly table-looking way
by using `print(fa3)`.

Along with the automata, there are modules to
deal with data persistency. `reader` comes
with `read_fa_from(filepath: str)` to read
an automata from a file; `writer`, responsible
for saving FA into `.txt` files, does so with
its `write(FiniteAutomata)` function.

#### File formatting

An automata can be retrived from a file with
contents like this:

5
0
1,2
a,b
0,a,1
0,b,2
1,a,1
1,b,3
2,a,4
2,b,2
3,a,1
3,b,3
4,a,4
4,b,2

It **must** have its contents divided in 4 sections:

    1. states;
    2. initial;
    3. final;
    4. transitions.

Every section **has** to begin with "#".

### Grammars

WIP

### Regular Expressions (regex)

A regex can be turned into a FA from a hard-coded
string, as functions for retrieving single
strings from files would make things harder
to understand. The conversion process
from regex to FA is done by following the
Dragon Book algorithm for Lexical Analysis.

The `format` module is used only to prepare
the regexes to be scanned, e.g. adds missing
concatenations between operators. The crowl
jewelry are the `conversion` and `tree` modules.

The `tree` module is responsible for building
a `SyntaxTree` from a given regex. The said tree
works as a binary tree, with every node being
a symbol from the regex, that is scanned from
*right to left*. If wanted, it can be viewed
by using `show_tree_from(root: Node)` function.
From `(&|b)(ab)*(&|a)`, the following tree
can be obtained.

![Tree from (&|b)(ab)*(&|a)](images/regex.png "Tree from (&|b)(ab)*(&|a)")

The `conversion` module will create a
`SyntaxTree` from a given regex and build
its FA equivalent. Using `fa_from(regex: str)`,
one can retrieve its automata.

![Fa from (&|b)(ab)*(&|a)](images/fa_from_regex.png "Fa from (&|b)(ab)*(&|a)")
