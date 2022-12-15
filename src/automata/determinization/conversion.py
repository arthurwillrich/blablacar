from src.automata.structures.fa import FiniteAutomata
from src.automata.persistency.reader import read_fa_from, new_read_fa_from
from src import resource_dir
from src.automata.structures.state import State


def determinize(nfa) -> FiniteAutomata:
    result = FiniteAutomata()

    closured_states = closure_states_for(nfa)

    result.initial_state = closured_states[nfa.initial_state]
    result.states = {result.initial_state}
    result.alphabet = nfa.alphabet

    stack = {closured_states[nfa.initial_state]}

    while stack:
        top = stack.pop()

        for pair, arrival in __transitions_for(nfa, top).items():
            if closured_states.get(arrival):  # If it has an entry, needs to be changed by its own closure.
                arrival = closured_states[arrival]

            if pair not in result.transitions.keys():
                result.transitions[pair] = {arrival}
                result.states |= {arrival}
                stack.add(arrival)

    result.final_states = __finals(nfa.final_states, result.states)
    __remove_useless_states_from(result)

    return result


def __finals(old_finals: set, all_states: set) -> set:
    final_states = set()

    for oldie in old_finals:
        for newly in all_states:
            if oldie.label in newly.label:
                final_states |= {newly}

    return final_states


def __remove_useless_states_from(automata: FiniteAutomata):
    """Removes empty transitions and states without labels
    from the :param automata."""
    copy = dict(automata.transitions)

    for transition, arrrival in copy.items():
        state, symbol = transition

        for destiny in arrrival:
            if symbol == '&' or destiny.label == '':
                del automata.transitions[transition]

        if state.label == '':
            automata.states.discard(state)


def closure_states_for(nfa: FiniteAutomata) -> dict:
    closure_states = dict()
    epsilon_closure: dict = epsilon_closure_from(nfa)

    for src, dst in epsilon_closure.items():
        state = __squash(dst)
        closure_states[src] = state

    return closure_states


def __squash(states: set) -> State:
    """Digests a :param state set: into a single :return state."""

    label = sorted([state.label for state in states])
    squashed = ''.join(label)
    return State(squashed)


def epsilon_closure_from(nfa: FiniteAutomata) -> dict:
    stack = [state for state in nfa.states]

    epsilon_closure = {state: {state} for state in nfa.states}
    empty_transitions = empty_transitions_from(nfa)

    while stack:
        top = stack.pop(0)

        for state in empty_transitions[top]:
            if state not in epsilon_closure[top]:
                epsilon_closure[top] |= epsilon_closure[state]
                stack.append(state)

    return epsilon_closure


def empty_transitions_from(nfa):
    empty_transitions = {state: set() for state in nfa.states}

    for transition, arrival in nfa.transitions.items():
        src_state, symbol = transition

        if symbol == '&':
            empty_transitions[src_state] |= arrival

    return empty_transitions


def __transitions_for(nfa, state: State) -> dict:
    """Gathers every possible transition from a :param state
    in the given :param nfa."""
    transitions = dict()

    for s in nfa.symbols():
        new_destiny = set()

        for transition, arrival in nfa.transitions.items():
            src_state, symbol = transition

            for label in state.label:
                if src_state == State(label) and symbol == s:
                    new_destiny |= arrival

        transitions[(state, s)] = __squash(new_destiny)

    return transitions


if __name__ == '__main__':
    # stub = read_fa_from(resource_dir / 'stub.txt')
    #
    # print(stub)
    # stub = determinize(stub)


    fa1 = new_read_fa_from('uniao1.txt')
    # print(fa1.alphabet)

    fa2 = new_read_fa_from('uniao2.txt')
    # print(fa2)

    # print(fa1)
    # print(fa2)

    uniao = (fa1 | fa2)
    uniao = determinize(uniao)

    print(uniao)

    # print(fa1 | fa2)
    # write(fa1 | fa2)




    # print(stub)
