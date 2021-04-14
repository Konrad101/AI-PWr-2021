from algorithm.csp import CSP
from secondProblem.einstein_riddle_constraint import RiddleConstraint
from secondProblem.house import House
from secondProblem.sentence import Sentence


def create_csp_einstein_riddle_problem():
    owners = [Sentence("owner", "Niemiec"),
              Sentence("owner", "Norweg"),
              Sentence("owner", "Szwed"),
              Sentence("owner", "Anglik"),
              Sentence("owner", "Duńczyk")]
    colors = [Sentence("color", "Niebieski"),
              Sentence("color", "Zielony"),
              Sentence("color", "Czerwony"),
              Sentence("color", "Żółty"),
              Sentence("color", "Biały")]
    drinks = [Sentence("drink", "Mleko"),
              Sentence("drink", "Piwo"),
              Sentence("drink", "Woda"),
              Sentence("drink", "Kawa"),
              Sentence("drink", "Herbata")]
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
    variables += drinks
    variables += owners
    variables += animals
    variables += colors
    variables += smokes

    first_house = House(1)
    second_house = House(2)
    third_house = House(3)
    fourth_house = House(4)
    fifth_house = House(5)
    houses = [first_house, second_house, third_house, fourth_house, fifth_house]
    domains = {}
    for variable in variables:
        domains[variable] = [first_house, second_house, third_house, fourth_house, fifth_house]

    csp = CSP(variables, domains)
    # Norweg zamieszkuje pierwszy dom
    domains[owners[1]] = [houses[0]]
    # W środkowym domu pija się mleko
    domains[drinks[0]] = [houses[2]]
    # Norweg mieszka obok niebieskiego domu
    domains[colors[0]] = [houses[1]]

    # dwie zaleznosci dotyczace jednego domu
    csp.append_constraint(RiddleConstraint(owners[3], colors[2]))
    csp.append_constraint(RiddleConstraint(drinks[4], owners[4]))
    csp.append_constraint(RiddleConstraint(smokes[1], colors[3]))
    csp.append_constraint(RiddleConstraint(owners[0], smokes[0]))
    csp.append_constraint(RiddleConstraint(smokes[3], animals[3]))
    csp.append_constraint(RiddleConstraint(owners[2], animals[0]))
    csp.append_constraint(RiddleConstraint(drinks[3], colors[1]))
    csp.append_constraint(RiddleConstraint(smokes[4], drinks[1]))

    # zaleznosci domow obok siebie
    csp.append_constraint(RiddleConstraint(colors[1], colors[4], neighbours=True, left_side_neighbour=True))
    csp.append_constraint(RiddleConstraint(smokes[2], animals[2], neighbours=True))
    csp.append_constraint(RiddleConstraint(smokes[2], drinks[2], neighbours=True))
    csp.append_constraint(RiddleConstraint(animals[1], colors[3], neighbours=True))

    return csp


def print_csp_einstein_riddle_solution(solution):
    if solution is not None:
        solution = dict(sorted(solution.items(), key=lambda item: item[1].number))
        solution = dict(sorted(solution.items(), key=lambda item: item[0].type, reverse=True))

        spacing = 22
        houses = {}
        for k, v in solution.items():
            if v not in houses:
                house_name = "House " + str(v.number)
                print(f'{house_name:{spacing}}', end="")
                houses[v] = None

        last_house = None
        print()
        for k, v in solution.items():
            if last_house is not None and last_house.number == len(houses):
                print()
            print(f'{k.value:{spacing}}', end="")
            last_house = v
    else:
        print("Solution not found")


def get_csp_arcs(csp: CSP):
    arcs = []
    for v, value_constraints in csp.constraints.items():
        for constraint in value_constraints:
            x, y = constraint.get_x_y()
            arcs.append(constraint)
            arcs.append(RiddleConstraint(y, x, constraint.neighbours, constraint.left_side_neighbour))

    return arcs


def get_initial_assignments():
    assignments = {Sentence("owner", "Norweg"): House(1),
                   Sentence("drink", "Mleko"): House(3),
                   Sentence("color", "Niebieski"): House(2)}
    return assignments
