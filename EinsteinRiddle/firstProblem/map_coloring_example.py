from algorithm.csp import CSP
from firstProblem.map_coloring_constraint import MapColoring


def create_csp_map_color_problem():
    variables = ["Dolnośląskie", "Lubuskie", "Wielkopolskie", "Opolskie",
                 "Łódzkie", "Śląskie", "Świętokrzyskie", "Małopolskie"]
    domains = {}
    for variable in variables:
        domains[variable] = ["red", "green", "blue"]
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


def initialize_first_values(csp: CSP):
    max_domain = []
    values = []
    for k, v in csp.domains.items():
        value_domain_size = len(v)
        values.append(k)
        if value_domain_size > len(max_domain):
            max_domain = v

    for i in range(0, len(max_domain) - 1):
        csp.domains[values[i]] = [max_domain[i]]


def get_csp_arcs(csp: CSP):
    arcs = []
    for v, value_constraints in csp.constraints.items():
        for constraint in value_constraints:
            x, y = constraint.get_x_y()
            arcs.append(constraint)
            arcs.append(MapColoring(y, x))

    return arcs
