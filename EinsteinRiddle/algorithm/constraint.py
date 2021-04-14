from abc import abstractmethod, ABC
from typing import Generic, TypeVar

V = TypeVar('V')
D = TypeVar('D')


class Constraint(Generic[V, D], ABC):
    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        pass

    @abstractmethod
    def get_x_y(self):
        pass
