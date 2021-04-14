import firstProblem.map_coloring_example as coloring_example
import secondProblem.einstein_riddle_example as riddle_example


def print_csp_solution(solution):
    if solution is not None:
        for s in solution:
            print(s, solution[s])
    else:
        print("Solution not found")


def test_csp_backtracking():
    print("Map coloring, Backtracking")
    csp_map_color = coloring_example.create_csp_map_color_problem()
    print_csp_solution(csp_map_color.backtracking_search())

    print("\nEinstein riddle, Backtracking")
    csp_einstein_riddle = riddle_example.create_csp_einstein_riddle_problem()
    riddle_example.print_csp_einstein_riddle_solution(csp_einstein_riddle.backtracking_search())


def test_csp_ac3():
    print("Map coloring, AC-3:")
    csp_map_color = coloring_example.create_csp_map_color_problem()
    coloring_example.initialize_first_values(csp_map_color)
    csp_map_color.ac3(coloring_example.get_csp_arcs(csp_map_color))
    print(csp_map_color.domains)


def test_forward_checking():
    heuristics = ["firstUnassigned", "mostConstraints"]
    heuristics_of_domain = ["random", "leastUsed"]

    for heuristic in heuristics:
        for heuristic_of_domain in heuristics_of_domain:
            print(f"\nMap coloring, Forward-checking, {heuristic}, {heuristic_of_domain}:")
            csp_map_color = coloring_example.create_csp_map_color_problem()
            result = csp_map_color.forward_checking(heuristic=heuristic, heuristic_of_domain=heuristic_of_domain)
            print(result)


if __name__ == "__main__":
    # test_csp_backtracking()
    test_csp_ac3()
    test_forward_checking()
