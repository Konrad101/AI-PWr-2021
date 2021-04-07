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
    variables = [
        Sentence("owner", "Norweg"),    # 0
        Sentence("owner", "Anglik"),    # 1
        Sentence("owner", "Duńczyk"),   # 2
        Sentence("owner", "Szwed"),     # 3
        Sentence("owner", "Niemiec"),   # 4

        Sentence("color", "Zielony"),   # 5
        Sentence("color", "Czerwony"),  # 6
        Sentence("color", "Żółty"),     # 7
        Sentence("color", "Niebieski"), # 8
        Sentence("color", "Biały"),     # 9

        Sentence("drink", "Piwo"),      # 10
        Sentence("drink", "Woda"),      # 11
        Sentence("drink", "Kawa"),      # 12
        Sentence("drink", "Herbata"),   # 13
        Sentence("drink", "Mleko"),     # 14

        Sentence("smoke", "Fajka"),     # 15
        Sentence("smoke", "Cygaro"),    # 16
        Sentence("smoke", "Papierosy light"),   # 17
        Sentence("smoke", "Papierosy bez filtra"),  #18
        Sentence("smoke", "Mentolowe"), #19

        Sentence("animals", "Psy"),     # 20
        Sentence("animals", "Konie"),   # 21
        Sentence("animals", "Koty"),    # 22
        Sentence("animals", "Ptaki"),   # 23
        Sentence("animals", "Rybki"),   # 24
    ]

    houses = [House(1), House(2), House(3), House(4), House(5)]
    domains = {}
    for variable in variables:
        domains[variable] = houses

    csp = CSP(variables, domains)

    # zaleznosci znane
    # Norweg zamieszkuje pierwszy dom
    domains[variables[0]] = [houses[0]]
    # W środkowym domu pija się mleko
    domains[variables[14]] = [houses[2]]
    # Norweg mieszka obok niebieskiego domu
    domains[variables[8]] = [houses[1]]

    # dwie zaleznosci dotyczace jednego domu
    csp.append_constraint(RiddleConstraint(variables[1], variables[6]))
    csp.append_constraint(RiddleConstraint(variables[13], variables[2]))
    csp.append_constraint(RiddleConstraint(variables[16], variables[7]))
    csp.append_constraint(RiddleConstraint(variables[4], variables[15]))
    csp.append_constraint(RiddleConstraint(variables[18], variables[23]))
    csp.append_constraint(RiddleConstraint(variables[3], variables[20]))
    csp.append_constraint(RiddleConstraint(variables[12], variables[5]))

    # zaleznosci domow obok siebie
    csp.append_constraint(RiddleConstraint(variables[5], variables[9], neighbours=True, left_side_neighbour=True))
    csp.append_constraint(RiddleConstraint(variables[17], variables[22], neighbours=True))
    csp.append_constraint(RiddleConstraint(variables[17], variables[11], neighbours=True))
    csp.append_constraint(RiddleConstraint(variables[21], variables[7], neighbours=True))

    return csp


def print_csp_solution(csp):
    solution = csp.backtracking_search()
    if solution is not None:
        for s in solution:
            print(s, solution[s])
        # print(solution)
    else:
        print("Solution not found")


if __name__ == "__main__":
    csp_map_color = create_csp_einstein_riddle_problem()
    #csp_map_color = create_csp_map_color_problem()
    print_csp_solution(csp_map_color)
