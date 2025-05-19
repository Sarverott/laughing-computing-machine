from deap import algorithms, creator, base, tools
import random
from tickable import evaluatory

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_perm", random.sample, range(9), 9)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_perm)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluatory.chaos_evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=50)

algorithms.eaSimple(
    population, toolbox,
    cxpb=0.5, mutpb=0.2,
    ngen=40,
    stats=None,
    halloffame=None,
    verbose=True
)
