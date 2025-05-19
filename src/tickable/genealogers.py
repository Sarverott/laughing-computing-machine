from deap import algorithms, creator, base, tools
import random
from tickable import resolvers, games, defines
import numpy

#global_record = []

def chaos_evaluate(individual):
    antagonist = resolvers.EvolutionAgent(individual, char="X", name="Evo")
    protagonist = resolvers.ChaosAgent(char="O", name="Chaos")

    game = games.TicTacToe(antagonist, protagonist)

    while not game.ended and game.turn < 9:
        game.play_turn()

    state = game.state(playername="antagonist")
    if state["winner"] == antagonist.char:
        #global_record.append([game.movestory, game.statestory, individual])
        return (1.0,)
    elif state["winner"] == protagonist.char:
        #global_record.append([game.movestory, game.statestory, individual])
        return (0.0,)
    else:
        #global_record.append([game.movestory, game.statestory, individual])
        return (0.5,)

class MutatorManager: # to można przerobić na PopulationManager
    def __init__(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.population = None
        self.evolver = None
        self.toolbox = base.Toolbox()
        self.fitness_history = []
        self.preference_census = []
    
    def configure(self):
        self.toolbox.register(
            "attr_perm",
            random.sample, range(9), 9
        )
        self.toolbox.register(
            "individual",
            tools.initIterate, creator.Individual, self.toolbox.attr_perm
        )
        self.toolbox.register(
            "population",
            tools.initRepeat, list, self.toolbox.individual
        )
        self.toolbox.register(
            "mate",
            tools.cxTwoPoint
        )

    def generate(self, evaluator, population, generations):
        # --- Symulacja ewolucji + agregacja statystyk ---
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
        self.toolbox.register("evaluate", evaluator)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        pop_list = self.toolbox.population(n=population)
        self.fitness_history = []
        self.preference_census = []

        for gen in range(generations):
            offspring = algorithms.varAnd(pop_list, self.toolbox, cxpb=0.5, mutpb=0.2)
            fits = list(map(self.toolbox.evaluate, offspring))
            for ind, fit in zip(offspring, fits):
                ind.fitness.values = fit
            pop_list = self.toolbox.select(offspring, k=len(pop_list))

            # --- Statystyki generacyjne ---
            fitness_vals = [ind.fitness.values[0] for ind in pop_list]
            self.fitness_history.append(fitness_vals)

            # Preferencje strategii dla heatmapy (agregujemy "pierwsze ruchy")
            first_move_counts = numpy.zeros(9)
            for ind in pop_list:
                first_move_counts[ind[0]] += 1
            preferences = first_move_counts.reshape(3, 3)
            self.preference_census.append(preferences)

        return {
            "fit_story": self.fitness_history,
            "census": self.preference_census[-1]
        }
        # --- Wywołanie game_predictions() dla ostatniego pokolenia ---
        #final_hist = {
        #    "win": np.clip(np.mean(fitness_history, axis=0), 0, 1),
        #    "lose": 1 - np.clip(np.mean(fitness_history, axis=0), 0, 1)
        #}
        #final_prefs = preference_census[-1]

    # def cohord_evolve(self, evaluator, population, generations):
    #     self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    #     self.toolbox.register("evaluate", evaluator)
    #     self.toolbox.register("select", tools.selTournament, tournsize=3)
    #     self.population = self.toolbox.population(n=population)
        
    #     self.evolver = algorithms.eaSimple(
    #         self.population, self.toolbox,
    #         cxpb=0.5, mutpb=0.2,
    #         ngen=generations,
    #         stats=None,
    #         halloffame=None,
    #         verbose=True
    #     )
        



