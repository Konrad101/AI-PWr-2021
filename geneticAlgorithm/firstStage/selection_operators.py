from random import Random


def tournament_operator(population, population_percentage=0.3):
    n = int(len(population) * population_percentage)
    if n == 0:
        n = 1

    selected_individuals = []
    while len(selected_individuals) < n:
        random_individual = population[Random().randint(0, len(population) - 1)]
        if not selected_individuals.__contains__(random_individual):
            selected_individuals.append(random_individual)

    best_individual = population[0]
    best_quality = population[0].evaluate_board(False)
    for individual in selected_individuals:
        individual_quality = individual.evaluate_board(False)
        if individual_quality < best_quality:
            best_individual = individual
            best_quality = individual_quality

    return best_individual


def roulette_operator(population):
    # slownik - { board: (widelki_dol, widelki_gora) }
    population_brackets = {}
    population_values = {}
    overall_sum = 0
    for individual in population:
        quality = individual.evaluate_board(False)
        overall_sum += quality
        population_values[individual] = quality

    # wartosc poprzedniego + wartosc aktualnego i jakies widelki
    last_individual_quality = 0
    for individual in population:
        lower_value = last_individual_quality
        if population.index(individual) == len(population) - 1:
            higher_value = 1
        else:
            higher_value = last_individual_quality + (1 - (population_values[individual] / overall_sum))
        population_brackets[individual] = (lower_value, higher_value)
        last_individual_quality = higher_value

    individual_value = Random().random()
    for key, value in population_brackets.items():
        lower_value, higher_value = value
        if lower_value <= individual_value <= higher_value:
            return key
