from algorithm.csp import CSP
from firstProblem.map_coloring_constraint import MapColoring
from secondProblem.einstein_riddle_constraint import RiddleConstraint
from secondProblem.house import House
from secondProblem.sentence import Sentence


def create_csp_map_color_problem():
    variables = ["Dolnośląskie", "Lubuskie", "Wielkopolskie", "Opolskie",
                 "Łódzkie", "Śląskie", "Świętokrzyskie", "Małopolskie"]
    domains = {}
    for variable in variables:
        domains[variable] = ["red", "green", "blue", "yellow"]
    csp = CSP(variables, domains)
    csp.append_constraint(MapColoring("Dolnośląskie", "Lubuskie"))
    csp.append_constraint(MapColoring("Dolnośląskie", "Wielkopolskie"))
    csp.append_constraint(MapColoring("Dolnośląskie", "Opolskie"))
    csp.append_constraint(MapColoring("Opolskie", "Łódzkie"))
    csp.append_constraint(MapColoring("Opolskie", "Śląskie"))
    csp.append_constraint(MapColoring("Opolskie", "Wielkopolskie"))
    csp.append_constraint(MapColoring("Śląskie", "Łódzkie"))
    csp.append_constraint(MapColoring("Śląskie", "Świętokrzyskie"))
    csp.append_constraint(MapColoring("Śląskie", "Małopolskie"))
    csp.append_constraint(MapColoring("Lubuskie", "Wielkopolskie"))
    csp.append_constraint(MapColoring("Wielkopolskie", "Łódzkie"))
    csp.append_constraint(MapColoring("Świętokrzyskie", "Łódzkie"))
    csp.append_constraint(MapColoring("Świętokrzyskie", "Małopolskie"))

    return csp


def create_csp_einstein_riddle_problem():
    owners = [Sentence("owner", "Norweg"),
              Sentence("owner", "Anglik"),
              Sentence("owner", "Duńczyk"),
              Sentence("owner", "Szwed"),
              Sentence("owner", "Niemiec")]
    colors = [Sentence("color", "Zielony"),
              Sentence("color", "Czerwony"),
              Sentence("color", "Żółty"),
              Sentence("color", "Niebieski"),
              Sentence("color", "Biały")]
    drinks = [Sentence("drink", "Piwo"),
              Sentence("drink", "Woda"),
              Sentence("drink", "Kawa"),
              Sentence("drink", "Herbata"),
              Sentence("drink", "Mleko")]
    smokes = [Sentence("smoke", "Fajka"),
              Sentence("smoke", "Cygaro"),
              Sentence("smoke", "Papierosy light"),
              Sentence("smoke", "Papierosy bez filtra"),
              Sentence("smoke", "Mentolowe")]
    animals = [Sentence("animals", "Psy"),
               Sentence("animals", "Konie"),
               Sentence("animals", "Koty"),
               Sentence("animals", "Ptaki"),
               Sentence("animals", "Rybki")]

    variables = []
    variables += colors
    variables += smokes
    variables += drinks
    variables += owners
    variables += animals

    houses = [House(1), House(2), House(3), House(4), House(5)]
    domains = {}
    for variable in variables:
        domains[variable] = houses

    csp = CSP(variables, domains)
    # zaleznosci znane
    # Norweg zamieszkuje pierwszy dom
    domains[owners[0]] = [houses[0]]
    # W środkowym domu pija się mleko
    domains[drinks[4]] = [houses[2]]
    # Norweg mieszka obok niebieskiego domu
    domains[colors[3]] = [houses[1]]

    # dwie zaleznosci dotyczace jednego domu
    csp.append_constraint(RiddleConstraint(owners[1], colors[1]))
    csp.append_constraint(RiddleConstraint(drinks[3], owners[2]))
    csp.append_constraint(RiddleConstraint(smokes[1], colors[2]))
    csp.append_constraint(RiddleConstraint(owners[4], smokes[0]))
    csp.append_constraint(RiddleConstraint(smokes[3], animals[3]))
    csp.append_constraint(RiddleConstraint(owners[3], animals[0]))
    csp.append_constraint(RiddleConstraint(drinks[2], colors[0]))

    csp.append_constraint(RiddleConstraint(owners[3], animals[4], opposite_sentences=True))

    # zaleznosci domow obok siebie
    csp.append_constraint(RiddleConstraint(colors[0], colors[4], neighbours=True, left_side_neighbour=True))
    csp.append_constraint(RiddleConstraint(smokes[2], animals[2], neighbours=True))
    csp.append_constraint(RiddleConstraint(smokes[2], drinks[1], neighbours=True))
    csp.append_constraint(RiddleConstraint(animals[1], colors[2], neighbours=True))

    return csp


def print_csp_solution(csp):
    solution = csp.backtracking_search()
    if solution is not None:
        for s in solution:
            print(s, solution[s])
    else:
        print("Solution not found")


def print_csp_einstein_riddle_solution(einstein_riddle_csp):
    solution = einstein_riddle_csp.backtracking_search()
    if solution is not None:
        solution = dict(sorted(solution.items(), key=lambda item: item[1].number))
        last_house = None
        for k, v in solution.items():
            if v != last_house:
                print()
            print(k, v)
            last_house = v
    else:
        print("Solution not found")


if __name__ == "__main__":
    csp_map_color = create_csp_map_color_problem()
    print_csp_solution(csp_map_color)

    csp_einstein_riddle = create_csp_einstein_riddle_problem()
    print_csp_einstein_riddle_solution(csp_einstein_riddle)
