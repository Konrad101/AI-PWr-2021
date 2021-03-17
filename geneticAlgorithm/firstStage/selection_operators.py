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


last_population = None
# jezeli populacja ta sama to nie przygotowywuj danych, tylko korzystaj z zapisanych


def roulette_operator(population):
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

    individual_value = Random().random()
    for key, value in population_values.items():
        if value[1] <= individual_value <= value[2]:
            return key
