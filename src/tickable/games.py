import numpy
from tickable import helpers, defines


class TicTacToe:
    
    movestory = []
    statestory = []
    
    board = None
    starts = "me"
    turn = 0
    ended = False
    scopes_state = None
    wins = None
    
    def game_state_detection(self):
        self.scopes_state = gamestate(self)

    def __init__(self):
        self.board = space["room"].copy()
    
    def update(self):
        self.game_state_detection()
        self.selfcheck()
        if self.statestory[-1] != self.scopes_state:
            self.statestory.append(self.scopes_state)

    def move(self, player=None, place=[0, 0]):
        self.turn = self.turn + 1
        board_coords = place[0]*3 + place[1]
        self.board[board_coords] = humanish_view[player]
        self.movestory.append((player, place))

    def display_board(self):
        return numpy.reshape(self.board, (-1, 3))

    def endgame(self, reason, winner=None):
        
        if reason=="victory":
            pass
        if reason=="tie":
            pass
        if reason=="violation":
            pass
            # unallowed action like moves 
            # where occupated 
            # or not this turn for move by this player 
            # or move not own mark 

    def selfcheck(self):
        #print("DEBUG selfcheck", self.scopes_state)
        playable = False
        for linescope in self.scopes_state:
            #print("DEBUG selfcheck sais", linescope)
            if linescope[1] == 3:
                self.ended = True
                self.wins = machine_view[1]
                return (False, linescope)
            elif linescope[1] == -3:
                self.ended = True
                self.wins = machine_view[-1]
                return (False, linescope)
            else:
                if linescope[2][0] > 0:
                    playable = True
        if not playable:
            self.ended = True
            self.wins = machine_view[0]
            return (False, None)
        else:
            return (True, None)


    def state(self):
        whose_turn_it_is = [
            players[
                 namespace_view[self.starts]
            ][1],
            [
                players[namespace_view[not_starts]][1]
                for not_starts in namespace_view 
                if not_starts not in [self.starts, "void"]
            ][0]
        ]
        return {
            "me": players[namespace_view["me"]][1],
            "endgame": self.ended,
            "winner": self.wins,
            "now_plays": whose_turn_it_is[self.turn % 2],
            "turn": self.turn
        }
    
#class TTT_player(TicTacToe):
