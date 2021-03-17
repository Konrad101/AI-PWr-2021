from crossover import crossover_operator
from data_loader import get_file_data
from generator.population_file_generator import save_population_to_file
from generator.population_file_reader import get_population_from_file
from generator.random_generator import generate_random_population
from genetic_algorithm import search_for_best_solution
from mutation import mutation_operator
from selection_operators import tournament_operator, roulette_operator

DATA_PATH = "data/zad0.txt"


def main():
    population_size = 100
    width, height, points = get_file_data(DATA_PATH)

    population = generate_random_population(population_size, width, height, points)
    # population = get_population_from_file("generated_population_100.txt")

    best_solution = search_for_best_solution(population)
    print(best_solution.evaluate_board())

    # save_population_to_file(population_size, width, height, points)

    '''child = crossover_operator(population[0], population[1])
    print("Parent 1", population[0].evaluate_board(False))
    print("Parent 2", population[1].evaluate_board(False))
    print("Child", child.evaluate_board(False))
    child = mutation_operator(child)
    print("Child after mutation", child.evaluate_board(False))'''

    '''best_individual = tournament_operator(population, 0.3)
    print("Tournament Quality:", best_individual.evaluate_board(), end="\n\n")

    best_individual = roulette_operator(population)
    print("Roulette Quality:", best_individual.evaluate_board())'''

    '''for i in range(0, len(population)):
        print()
        print("Individual", i + 1)
        res = population[i].evaluate_board()
        print("Adaptation ratio:", res)'''


if __name__ == "__main__":
    main()
