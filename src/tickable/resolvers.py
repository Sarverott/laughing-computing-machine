import numpy
import random
from tickable import games, defines, helpers
from collections import defaultdict

games_record = []
moves_mapping = []

class PlayerAgent:
    char = ""  # numpy. "X" lub "O"
    name = "undefined"  # identyfikator do movestory
    def choose_move(self, game):
        raise NotImplementedError

class ChaosAgent(PlayerAgent):
    def __init__(self, char="O", name="Chaos"):
        self.char = char
        self.name = name

    def choose_move(self, game):
        empty_cells = [i for i, val in enumerate(game.board) if val == 0]
        if empty_cells:
            rand_move = random.choice(empty_cells)
            return (True, divmod(rand_move, 3))
        return (False, None)

class EvolutionAgent(PlayerAgent):
    def __init__(self, genome, char="X", name="Evo"):
        self.genome = genome  # permutacja 0–8
        self.cursor = 0
        self.char = char
        self.name = name

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


def extract_reactive_signature(gamestate_vector, move):
    """
    Tworzy podpis reaktywnego ruchu:
    - znormalizowane wektory stanu (gamestate),
    - pozycję ruchu (x, y),
    - sygnatury do indeksowania.

    Zwraca:
    {
        "reaction": (x, y),
        "state_signature": {
            "avg": [...],
            "sum": [...],
            "owners": [...]
        }
    }
    """
    avg_vector = [int(round((v[0] + 4) * 100)) for v in gamestate_vector]  # przesunięcie + zaokrąglenie
    sum_vector = [int(v[1] + 4) for v in gamestate_vector]                # z -3/3 do 1/7
    owner_counts = [tuple(v[2]) for v in gamestate_vector]                # numpy. (0, 1, 2)

    signature = {
        "reaction": tuple(move),
        "state_signature": {
            "avg": avg_vector,
            "sum": sum_vector,
            "owners": owner_counts
        }
    }

    return signature

# def build_tactic_index(games=games_record, winner_name="Evo"):
#     """
#     Buduje indeks taktyczny z listy gier:
#     - Dla każdego ruchu tworzy podpis reaktywny.
#     - Grupuje dane pod względem skuteczności (win/loss) tego ruchu z danego stanu.

#     Parameters:
#         games: lista obiektów TicTacToe lub kompatybilnych z .movestory i .board
#         helpers_module: moduł zawierający funkcję `gamestate(game)`
#         winner_name: imię gracza, którego ruchy traktujemy jako "zwycięskie"

#     Returns:
#         tactic_index: dict[signature_hash][reaction] -> {"win": N, "loss": M}
#     """
#     tactic_index = defaultdict(lambda: defaultdict(lambda: {"win": 0, "loss": 0}))

#     # for game in games:
#     #     for turn_idx, (who, move) in enumerate(game.movestory):
#     #         # zapamiętujemy stan planszy PRZED ruchem
#     #         gamestate_vector = helpers.gamestate(game)

#     #         signature = extract_reactive_signature(gamestate_vector, move)
#     #         sig_key = (
#     #             tuple(signature["state_signature"]["avg"]),
#     #             tuple(signature["state_signature"]["sum"]),
#     #             tuple(signature["state_signature"]["owners"])
#     #         )
#     #         reaction = signature["reaction"]

#     #         # aktualizujemy planszę (po ruchu)
#     #         coord = move[0] * 3 + move[1]
#     #         current_board[coord] = -1 if who == "Evo" else 1

#     #         # aktualizuj statystykę skuteczności
#     #         outcome_key = "win" if game.wins == ("X" if winner_name == "Evo" else "O") else "loss"
#     #         tactic_index[sig_key][reaction][outcome_key] += 1

#     return tactic_index

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
