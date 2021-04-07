from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Dict

V = TypeVar('V')
D = TypeVar('D')


class Constraint(Generic[V, D], ABC):
    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        pass


class CSP(Generic[V, D]):
    def __init__(self, variables, domains):
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
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

        if len(assignment) == len(self.variables):
            return assignment

        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        first: V = unassigned[0]

        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None
