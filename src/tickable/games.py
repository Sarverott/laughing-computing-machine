import numpy
from tickable import defines, helpers, resolvers


class TicTacToe:
    movestory = []
    statestory = []
    board = None
    starts = "antagonist"
    turn = 0
    ended = False
    scopes_state = None
    wins = None

    def __init__(self, antagonist, protagonist):
        self.board = defines.space["room"].copy()
        self.turn = 0
        self.ended = False
        self.antagonist = antagonist
        self.protagonist = protagonist
        self.scopes_state = helpers.gamestate(self)
        resolvers.games_record.append(self)
        # inne pola jak poprzednio...

    def whose_turn_it_is(self):
        terms = [not self.turn % 2 == 0, self.starts == "antagonist"]
        return self.antagonist if terms[0] ^ terms[1] else self.protagonist 

    def play_turn(self):
        current_agent = self.whose_turn_it_is()
        is_moving, move = current_agent.choose_move(self)
        if is_moving and move:
            if resolvers.tactics_for == current_agent.name:
                tactic_sign = helpers.signat_for_statemove(self.scopes_state)
                if tactic_sign not in resolvers.moves_mapping:
                    resolvers.moves_mapping[tactic_sign] = list()
                resolvers.moves_mapping[tactic_sign].append([move, self], self)
            self.movestory.append((current_agent.name, move))
            self.move(current_agent.char, move)
            self.update()
        self.turn += 1

    def update(self):
        self.scopes_state = helpers.gamestate(self)
        self.selfcheck()
        self.statestory.append(self.scopes_state)

    def move(self, player=None, place=[0, 0]):
        board_coords = place[0]*3 + place[1]
        self.board[board_coords] = defines.humanish_view[player]

    def selfcheck(self):
        playable = False
        for linescope in self.scopes_state:
            if linescope[1] == 3:
                self.ended = True
                self.wins = defines.machine_view[1]
                return (False, linescope)
            elif linescope[1] == -3:
                self.ended = True
                self.wins = defines.machine_view[-1]
                return (False, linescope)
            else:
                if linescope[2][0] > 0:
                    playable = True
        if not playable:
            self.ended = True
            self.wins = defines.machine_view[0]
            return (False, None)
        else:
            return (True, None)

    def state(self, playername="antagonist"):
        return {
            "me": defines.players[defines.namespace_view[playername]][1],
            "endgame": self.ended,
            "winner": self.wins,
            "now_plays": self.whose_turn_it_is().char,
            "turn": self.turn
        }
