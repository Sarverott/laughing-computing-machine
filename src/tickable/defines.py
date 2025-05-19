import numpy

defines = [0, "", "void",
    1, "O", "protagonist",
    -1, "X", "antagonist"]

max_game_turns = 9

players = [
    (
        defines[3*i],
        defines[3*i+1],
        defines[3*i+2]
    ) for i in range(3)
]

algorithmish_view = [
    (
        defines[i], 
        defines[i+1]
    ) for i in range(0, len(defines), 3)
]


machine_view = dict(algorithmish_view)

humanish_view = {k: v for v, k in algorithmish_view}

namespace_view = {players[side][2]: side for side in range(len(players))}

space = {
    "D":len(players) - 1,
    "infotags": [ 
        "compatible for competition", 
        "minimal to be complementary",
        "including all sites without exceptions"
    ],
    "room":None
}

space["room"] = numpy.array(
    [players[0][0]]*(len(players)**space["D"]), # 5**5 == 5*5*5*5*5
    dtype = numpy.int8 # integers from -128 to 127
)