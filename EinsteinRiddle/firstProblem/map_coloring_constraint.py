from typing import Dict

from algorithm.csp import Constraint


class MapColoring(Constraint[str, str]):
    def __init__(self, first_location: str, second_location: str):
        super().__init__([first_location, second_location])
        self.first_location = first_location
        self.second_location = second_location

    def satisfied(self, assignment: Dict[str, str]):
        # jesli brak pierwszej lub drugiej lokalizacji to nie sprawdzaj
        if self.first_location not in assignment or self.second_location not in assignment:
            return True

        return assignment[self.first_location] != assignment[self.second_location]
