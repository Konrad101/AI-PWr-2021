from copy import deepcopy
from random import Random

from crossover import crossover_operator
from mutation import mutation_operator
from selection_operators import roulette_operator, tournament_operator

MAX_POPULATIONS_WITHOUT_CHANGE = 7
CROSSOVER_PROBABILITY = 0.77
SMALL_MUTATION_PROBABILITY = 0.5


def search_for_best_solution(population, max_populations, tournament=True):
    populations_without_change = 0
    best_quality = None
    best_child = None
    populations_data = []
    population_number = 1
    while (not best_individual_is_good_enough(best_child) or
           populations_without_change < MAX_POPULATIONS_WITHOUT_CHANGE) and population_number <= max_populations:
        new_population = []
        population_score = 0
        best_quality_from_last_population = best_quality
        while len(new_population) < len(population):
            if tournament:
                first_parent = tournament_operator(population, 0.05)
                second_parent = tournament_operator(population, 0.05)
            else:
                first_parent = roulette_operator(population)
                second_parent = roulette_operator(population)
            if Random().random() < CROSSOVER_PROBABILITY:
                child = crossover_operator(first_parent, second_parent)
            else:
                child = deepcopy(first_parent)
            child = mutation_operator(child, SMALL_MUTATION_PROBABILITY)
            child_evaluation = child.evaluate_board(False)
            population_score += child_evaluation
            new_population.append(child)
            if best_quality is None:
                best_quality = child_evaluation
                best_child = deepcopy(child)
            elif child_evaluation < best_quality:
                best_quality = child_evaluation
                best_child = deepcopy(child)

        if best_quality == best_quality_from_last_population:
            populations_without_change += 1
            # print("No changes:", populations_without_change)
        else:
            populations_without_change = 0
        # print("Population", population_number, " ", best_quality)
        population_data = __get_population_data(new_population, population_number)

        populations_data.append(population_data)
        population_number += 1
        population = new_population

    # print(best_quality)
    return best_child, populations_data


def best_individual_is_good_enough(best_individual):
    if best_individual is not None:
        if best_individual.get_intersections_amount() == 0 and best_individual.count_segments_over_board() == 0:
            return True
    return False


def __get_population_data(population, population_number):
    first_iteration = True
    best = 0
    worst = 0
    for individual in population:
        individual_value = individual.evaluate_board(False)
        if first_iteration:
            best = individual_value
            worst = individual_value
            first_iteration = False
        else:
            if individual_value < best:
                best = individual_value
            if individual_value > worst:
                worst = individual_value

    return population_number, best, worst
