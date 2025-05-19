import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from deap import creator, base, tools, algorithms
import random

# Przygotowanie środowiska DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_perm", random.sample, range(9), 9)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_perm)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Losowa funkcja oceny — tylko do symulacji wizualizacji
def dummy_evaluate(individual):
    return (random.uniform(0, 1),)

toolbox.register("evaluate", dummy_evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

