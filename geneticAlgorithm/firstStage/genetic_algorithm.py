from copy import deepcopy
from random import Random

from crossover import crossover_operator
from mutation import mutation_operator
from selection_operators import roulette_operator, tournament_operator

MAX_POPULATIONS_WITHOUT_CHANGE = 7
CROSSOVER_PROBABILITY = 0.67
SMALL_MUTATION_PROBABILITY = 0.5


def search_for_best_solution(population):
    populations_without_change = 0
    best_quality = None
    best_child = None
    population_number = 1
    while populations_without_change < MAX_POPULATIONS_WITHOUT_CHANGE:
        new_population = []
        best_quality_from_last_population = best_quality
        while len(new_population) < len(population):
            first_parent = tournament_operator(population, 0.25)
            second_parent = roulette_operator(population)
            if Random().random() < CROSSOVER_PROBABILITY:
                child = crossover_operator(first_parent, second_parent)
            else:
                child = deepcopy(first_parent)
            child = mutation_operator(child, SMALL_MUTATION_PROBABILITY)
            child_evaluation = child.evaluate_board(False)
            new_population.append(child)
            if best_quality is None:
                best_quality = child_evaluation
                best_child = deepcopy(child)
            elif child_evaluation < best_quality:
                best_quality = child_evaluation
                best_child = deepcopy(child)

        if best_quality == best_quality_from_last_population:
            populations_without_change += 1
            print("No changes -", populations_without_change)
        else:
            populations_without_change = 0
        print("Population", population_number, " ", best_quality)
        population_number += 1
        population = new_population
    print(best_quality)
    return best_child
