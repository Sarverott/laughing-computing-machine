from deap import algorithms, creator, base, tools
import random
from tickable import resolvers, games, defines

def chaos_evaluate(individual):
    agent = resolvers.EvolutionAgent(individual)
    opponent = resolvers.ChaosAgent()  # lub inny typ

    game = games.TicTacToe(agent, opponent)

    while not game.ended and game.turn < defines.max_game_turns:
        game.play_turn()

    state = game.state()
    if state["winner"] == "X":  # agent zawsze X, np. jako me
        return (1.0,)
    elif state["winner"] == "O":
        return (0.0,)
    return (0.5,)

class MutatorMachine:
    def __init__(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()

        self.toolbox.register("attr_perm", random.sample, range(9), 9)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.attr_perm)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
        
    def mutate(self, evaluator, population, generations):

        self.toolbox.register("evaluate", evaluator)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.population = self.toolbox.population(n=population)
        
        self.evolver = algorithms.eaSimple(
            self.population, self.toolbox,
            cxpb=0.5, mutpb=0.2,
            ngen=generations,
            stats=None,
            halloffame=None,
            verbose=True
        )
        



