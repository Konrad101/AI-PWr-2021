import random
from copy import deepcopy
from typing import Generic, List, Dict

from algorithm.constraint import V, D, Constraint


# algorytm zaimplementowany w oparciu o źródło:
# https://freecontent.manning.com/constraint-satisfaction-problems-in-python
class CSP(Generic[V, D]):
    def __init__(self, variables, domains):
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        self.__initialize_variables()

        self.__heuristic = "firstUnassigned"
        self.__heuristic_of_domain = "random"

    def __initialize_variables(self):
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Variable without domain error", variable)

    def append_constraint(self, constraint: Constraint[V, D]):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable not found:", variable)
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment=None):
        if assignment is None:
            assignment = {}

        # koniec rekursji, gdy kazda zmienna ma przypisana wartosc
        if len(assignment) == len(self.variables):
            return assignment

        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        # pierwsza zmienna, ktora nie ma przypisanej wartosci
        first: V = unassigned[0]

        # kazda wartosc z dziedziny wartosci
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            # do kopii przypisanych dodaje pierwszy nieprzypisany
            local_assignment[first] = value
            # jezeli wartosc nie przekracza ograniczen
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None

    def revise(self, x, y, assignments, arcs):
        revised = False
        x_domain = self.domains[x]
        y_domain = self.domains[y]

        x_constraints = []
        for constraint in arcs:
            if constraint.get_x_y()[0] == x and constraint.get_x_y()[1] == y:
                x_constraints.append(constraint)

        for x_value in x_domain:
            satisfies = False
            assignments[x] = x_value
            for y_value in y_domain:
                local_assignments = deepcopy(assignments)
                local_assignments[y] = y_value
                for constraint in x_constraints:
                    if constraint.satisfied(local_assignments):
                        satisfies = True
                        break
                if satisfies:
                    break

            if not satisfies:
                x_domain.remove(x_value)
                assignments.pop(x)
                revised = True

        return revised

    def ac3(self, arcs, assignments=None):
        queue = arcs[:]

        if assignments is None:
            assignments = {}
        while queue:
            # pierwszy arc z kolejki z ograniczeniami
            x, y = queue.pop(0).get_x_y()

            revised = self.revise(x, y, assignments, arcs)
            if revised:
                # dodaj do kolejki wszystkie ograniczenia sasiadow zmienionego wezla
                neighbors = [neighbor for neighbor in arcs if neighbor.get_x_y()[1] == x]
                queue = queue + neighbors

    def forward_checking(self, assignment=None):
        return self.__search_forward_checking(assignment)

    def __search_forward_checking(self, assignment):
        if assignment is None:
            assignment = {}

        if len(assignment) == len(self.variables):
            return assignment

        unassigned = self.__next_unassigned_variable(assignment)
        values = self.__available_domains(unassigned, assignment)
        if len(values) > 0:
            assignment[unassigned] = values[0]
            return self.__search_forward_checking(assignment)

        return None

    def __available_domains(self, variable, assignment):
        results = self.__available_values(self.domains[variable], assignment)
        if results is None or len(results) == 0:
            return []

        for d in assignment.values():
            local_assignment = deepcopy(assignment)
            local_assignment[variable] = d

            if not self.consistent(variable, local_assignment):
                if d in results:
                    results.remove(d)

        return results

    def __available_values(self, value_domain, assignment):
        if self.__heuristic_of_domain == "random":
            return self.__random_values(value_domain)
        elif self.__heuristic_of_domain == "leastUsed":
            return self.__least_used_values(value_domain, assignment)

    @staticmethod
    def __random_values(domain):
        random.shuffle(domain)
        return domain

    def __least_used_values(self, domains, assignment):
        values_with_amount = {}
        for d in domains:
            values_with_amount[d] = 0

        for d in assignment.values():
            values_with_amount[d] += 1

        values = []
        while len(values_with_amount) > 0:
            value = min(values_with_amount, key=values_with_amount.get)
            values.append(value)
            values_with_amount.pop(value)
        return values

    def __next_unassigned_variable(self, assignment):
        if self.__heuristic == "firstUnassigned":
            return self.__first_unassigned_variable(assignment)
        elif self.__heuristic == "mostConstraints":
            return self.__variable_with_most_constraints(assignment)

    def __first_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

        return None

    def __variable_with_most_constraints(self, assignment):
        unassigned = [variable for variable in self.variables if variable not in assignment]
        max_constraints = 0
        variable_with_most_constraints = None

        for variable in unassigned:
            constraints_amount = len(self.constraints[variable])
            if constraints_amount > max_constraints:
                max_constraints = constraints_amount
                variable_with_most_constraints = variable

        return variable_with_most_constraints
