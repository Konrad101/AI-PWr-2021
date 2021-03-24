import sys

import numpy

from board.board import PCBBoard
from board.path import Path
from board.segment import Segment, Direction
from chart_drawer import draw_chart
from data_loader import get_file_data
from generator.population_file_generator import save_population_to_file
from generator.population_file_reader import get_population_from_file
from generator.random_generator import generate_random_population
from genetic_algorithm import search_for_best_solution
from mutation import mutate_path_segment

TASK = "zad1"
DATA_PATH = "data/" + TASK + ".txt"
POPULATION_SIZE = 100
MAX_POPULATIONS = 500


def main():
    width, height, points = get_file_data(DATA_PATH)
    test_genetic_algorithm(3)
    # population = generate_random_population(POPULATION_SIZE, width, height, points)
    #best_solution = search_for_best_solution(population, max_populations)


def test_genetic_algorithm(iterations_amount):
    population = get_population_from_file(TASK + "/generated_population_" + str(POPULATION_SIZE) + ".txt")
    # avg - srednia z najwyzszych
    # worst - srednia z 10 najnizszych
    results = []
    for i in range(0, iterations_amount):
        best_solution = search_for_best_solution(population, MAX_POPULATIONS)
        print(best_solution[0].evaluate_board())
        results.append(best_solution[1])
    best_list = []
    worst_list = []
    avg_list = []
    values = []
    for i in range(MAX_POPULATIONS):
        best_list.append(sys.maxsize)
        worst_list.append(0)
        avg_list.append(0)
        values.append(i + 1)

    # results - lista list
    # result - lista wynikow z jednego dzialania
    worst_quality = 0
    for result in results:
        for population_data in result:
            avg_populations_score = 0
            worst_populations_score = 0
            population_number = population_data[0]
            for i in range(0, len(results)):
                best_population_score = results[i][population_number - 1][1]
                worst_population_quality = results[i][population_number - 1][2]
                if worst_population_quality > worst_quality:
                    worst_quality = worst_population_quality

                worst_populations_score += worst_population_quality
                avg_populations_score += best_population_score
                if best_population_score < best_list[population_number - 1]:
                    best_list[population_number - 1] = best_population_score
            avg_list[population_number - 1] = avg_populations_score / len(results)
            worst_list[population_number - 1] = worst_populations_score / len(results)

    print("BEST QUALITY:", round(min(best_list), 2))
    print("WORST QUALITY:", round(worst_quality, 2))
    print("AVG QUALITY:", round(sum(worst_list) / len(worst_list), 2))
    print("STD QUALITY:", round(numpy.std(worst_list), 2))

    draw_chart(best_list, worst_list, avg_list, values)



    '''segments = [Segment(1, Direction.down, 1, 3),
                Segment(4, Direction.right, 1, 4),
                Segment(1, Direction.up, 5, 4)]
    path = Path(1, 3, 5, 3, segments)
    path = mutate_path_segment(path, PCBBoard(6, 6))
    x = 1'''

    '''save_population_to_file(population_size, width, height, points, "zad3/generated_population_200.txt")
    save_population_to_file(100, width, height, points, "zad3/generated_population_100.txt")
    save_population_to_file(50, width, height, points, "zad3/generated_population_50.txt")'''


if __name__ == "__main__":
    main()
