import sys
from random import Random


def tournament_operator(population, population_percentage=0.073):
    n = int(len(population) * population_percentage)
    if n == 0:
        n = 1

    selected_individuals = Random().sample(population, n)

    best_individual = population[0]
    best_quality = sys.maxsize
    for individual in selected_individuals:
        individual_quality = individual.evaluate_board(False)
        if individual_quality < best_quality:
            best_individual = individual
            best_quality = individual_quality

    return best_individual


last_population_values = None
last_population = None


def roulette_operator(population):
    global last_population
    global last_population_values
    if last_population is None or last_population != population:
        population_values = __get_population_values(population)
    else:
        population_values = last_population_values

    individual_value = Random().random()

    last_population = population
    last_population_values = population_values

    for key, value in population_values.items():
        if value[1] <= individual_value <= value[2]:
            return key


def __get_population_values(population):
    # slownik - { board: (widelki_dol, widelki_gora) }
    population_values = {}
    overall_sum = 0
    for individual in population:
        quality = individual.evaluate_board(False)
        overall_sum += quality
        population_values[individual] = quality

    population_values = dict(sorted(population_values.items(), key=lambda item: item[1]))

    # wartosc poprzedniego + wartosc aktualnego i jakies widelki
    last_individual_quality = 0
    index = 0
    for key, value in population_values.items():
        lower_value = last_individual_quality
        if index == len(population) - 1:
            higher_value = 1
        else:
            higher_value = last_individual_quality + (population_values[key] / overall_sum)

        population_values[key] = (value, lower_value, higher_value)
        last_individual_quality = higher_value
        index += 1

    sorted_values_list = list(population_values.values())
    index = len(sorted_values_list) - 1
    for key, value in population_values.items():
        population_values[key] = value[0], sorted_values_list[index][1], sorted_values_list[index][2]
        index -= 1

    return population_values
