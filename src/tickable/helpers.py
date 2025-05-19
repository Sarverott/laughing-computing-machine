import numpy
from tickable import defines



def make_histogram(fitness_history, size=9):
    """
    Przekształca historię fitnessów z wielu generacji w histogram
    szansy na wygraną i przegraną dopasowany do długości wykresu f(x), g(x).

    Parameters:
        fitness_history (list of list): lista fitnessów z każdej generacji
        size (int): liczba punktów w osi x (domyślnie 9 = liczba tur w grze)

    Returns:
        dict: {"win": [...], "lose": [...]}
    """
    fitness_avg_per_gen = [numpy.mean(gen) if gen else 0.0 for gen in fitness_history]

    # Skalowanie do 'size' punktów
    if len(fitness_avg_per_gen) < size:
        # Dublowanie wartości jeśli za mało pokoleń
        expanded = numpy.interp(
            numpy.linspace(0, len(fitness_avg_per_gen) - 1, size),
            numpy.arange(len(fitness_avg_per_gen)),
            fitness_avg_per_gen
        )
    else:
        # Wybranie reprezentatywnych indeksów
        x_indices = numpy.linspace(0, len(fitness_avg_per_gen) - 1, size).astype(int)
        expanded = numpy.array(fitness_avg_per_gen)[x_indices]

    expanded = numpy.clip(expanded, 0, 1)

    return {
        "win": expanded,
        "lose": 1 - expanded
    }

def vector_scope(axisarray, actsides):
    # print("DEBUG:", actsides)
    # print("DEBUG:", axisarray)
    # print("DEBUG:", 
    #             [numpy.where(
    #                 axisarray == force
    #             )[0]
            
    #         for force in actsides])
    return [
        numpy.float16(
            numpy.average(axisarray)
        ),
        numpy.int8(
            numpy.sum(axisarray)
        ),
        [
            len(
                numpy.where(
                    axisarray == int(force)
                )[0]
            )
            for force in actsides
        ]
    ]

def axis_scoping(*single_or_many_arrays):
        output_list = []
        for axisarray in single_or_many_arrays:
            output_list.append(
                vector_scope(
                    axisarray, 
                    numpy.array(defines.players)[:, 0]
                )
            )
        if len(single_or_many_arrays) == 1:
            return output_list[0]
        else:
            return output_list
# ddd


def gamestate(game):
    matrix = numpy.reshape(game.board, (-1, 3))
    return axis_scoping(
        numpy.diag(matrix),
        numpy.diag(numpy.flip(matrix)),
        matrix[0, :],
        matrix[1, :],
        matrix[2, :],
        matrix[:, 0],
        matrix[:, 1],
        matrix[:, 2]
    )

def move_on_gamestate(at_state, maked_move): 
    # powinno przyjąć wynik gamestate przed ruchem 
    # i wykonany ruch w odpowiedzi
    state_avg_ptr = ",".join([round((avg[0]+4)*100) for avg in at_state])
    state_sum_ptr = ",".join([avg[1]+4 for avg in at_state])
    state_owners_ptr = ",".join(["".join(avg[2]) for avg in at_state])
    return [maked_move, state_avg_ptr, state_sum_ptr, state_owners_ptr]

def extract_reactive_signature(gamestate_vector, move):
    return {
        "reaction": move,
        "state_signature": {
            "avg": [round((v[0]+4)*100) for v in gamestate_vector],
            "sum": [v[1]+4 for v in gamestate_vector],
            "owners": [tuple(v[2]) for v in gamestate_vector]
        }
    }