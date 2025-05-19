import numpy
from tickable import defines

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