from typing import Dict

from algorithm.csp import Constraint
from secondProblem.house import House
from secondProblem.sentence import Sentence


class RiddleConstraint(Constraint[Sentence, Sentence]):
    def __init__(self, first_sentence, second_sentence):
        super().__init__([first_sentence, second_sentence])
        self.first_sentence = first_sentence
        self.second_sentence = second_sentence

    def satisfied(self, assignment: Dict[Sentence, House]):
        # czy powtarza sie dom dla takich samych typow (koloru, narodowosci itd)
        for s in assignment:
            for a in assignment:
                if s != a and s.type == a.type:
                    if assignment[s] == assignment[a]:
                        return False

        if self.first_sentence not in assignment or self.second_sentence not in assignment:
            return True

        # sprawdzenie czy pierwsza sentencja dotyczy tego samego domu co druga
        return assignment[self.first_sentence] == assignment[self.second_sentence]
