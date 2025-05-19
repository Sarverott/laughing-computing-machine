import numpy
import random
from tickable import games, defines

class PlayerAgent:
    char = ""
    name = "me"
    def choose_move(self, game):
        raise NotImplementedError

class ChaosAgent(PlayerAgent):
    def choose_move(self, game):
        empty_cells = [i for i, val in enumerate(game.board) if val == 0]
        if empty_cells:
            rand_move = random.choice(empty_cells)
            return (True, divmod(rand_move, 3))
        else:
            return (False, None)

class EvolutionAgent(PlayerAgent):
    def __init__(self, genome):
        self.genome = genome  # permutacja 0-8
        self.cursor = 0       # indeks aktualnego ruchu

    def choose_move(self, game):
        while self.cursor < len(self.genome):
            move = divmod(self.genome[self.cursor], 3)
            self.cursor += 1
            if game.board[move[0]*3 + move[1]] == 0:
                return (True, move)
        return (False, None)

class UserAgent(PlayerAgent):
    def choose_move(self, game):
        return (False, None)
    
class ReplayAgent(PlayerAgent):
    def choose_move(self, game):
        return (False, None)

class IntelligenceAgent(PlayerAgent):
    def choose_move(self, game):
        return (False, None)

def VoidAgent():
    return None


#def heuristic_move(game.board, strategy="centralized"):
#    pass

# def genetic_move(game, strategy="centralized"):

# def random_evaluate(individual):
#     game = tickable.games.TicTacToe() 
#     current_player = "me"
#     opponent = "you"
#     # Strategie: gracz sterowany przez DEAP gra jako "me"
#     move_index = 0
#     while not game.ended and move_index < 9:
#         move = divmod(individual[move_index], 3)  # indeks → współrzędne
#         print("DEBUG move", move, game.board[move[0]*3 + move[1]])
#         if game.board[move[0]*3 + move[1]] == 0:
#             game.move(
#                 games.players[
#                     games.namespace_view[
#                         current_player
#                     ]
#                 ][1], 
#                 list(move)
#             )
#             game.update()
#             move_index += 1
#             # Gra się skończyła?
#             if game.ended:
#                 break
#             # Ruch przeciwnika — losowy

#             empty_cells = [i for i, val in enumerate(game.board) if val == 0]
#             if empty_cells:
#                 enemy_choice = random.choice(empty_cells)
#                 move = divmod(enemy_choice, 3)
#                 game.move(
#                     games.players[
#                         games.namespace_view[
#                             opponent
#                         ]
#                     ][1], 
#                     list(move)
#                 )
#                 game.update()

#         else:
#             move_index += 1  # nielegalny ruch? pomijamy
#             print("DEBUG no legal", move_index, move)

#     state = game.state()
#     if state["winner"] == games.players[games.namespace_view[current_player]][1]:
#         #### here we have display how uneasy it is when we mix multiple ways of communication
#         return (1.0,)  # zwycięstwo
#     elif state["winner"] == games.players[games.namespace_view[opponent]][1]:
#         #### do tego dochodzą jeszcze dochodzi rozbieżność językowa ludzkiej mowy
#         return (0.0,)  # porażka
#     else:
#         return (0.5,)  # remis lub brak zwycięzcy
#         #### Wir haben so viel Arbeit mit der Mittelwertbildung und Anpassung 
#         #### der Daten an eine gemeinsame Form des Datenrealitätsplans, dass 
#         #### wir die Tatsache übersehen, dass es trotz zweier Spieler einen 
#         #### versteckten dritten Spieler gibt
