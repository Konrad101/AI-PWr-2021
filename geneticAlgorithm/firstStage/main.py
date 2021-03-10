from data_loader import get_file_data
from random_generator import generate_random_population

DATA_PATH = "data/zad3.txt"


def main():
    population_size = 100
    width, height, points = get_file_data(DATA_PATH)

    population = generate_random_population(population_size, width, height, points)
    for i in range(0, len(population)):
        print()
        print("Individual", i + 1)
        res = population[i].evaluate_board()
        print("Adaptation ratio:", res)


if __name__ == "__main__":
    main()
