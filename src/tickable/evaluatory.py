
from tickable import games, resolvers


def chaos_evaluate(individual):
    agent = resolvers.EvolutionAgent(individual)
    opponent = resolvers.ChaosAgent()  # lub inny typ

    game = games.TicTacToe(agent, opponent)

    while not game.ended and game.turn < 9:
        game.play_turn()

    state = game.state()
    if state["winner"] == "X":  # agent zawsze X, np. jako me
        return (1.0,)
    elif state["winner"] == "O":
        return (0.0,)
    return (0.5,)
