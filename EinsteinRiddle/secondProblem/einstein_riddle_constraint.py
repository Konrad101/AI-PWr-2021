from typing import Dict

from algorithm.csp import Constraint
from secondProblem.house import House
from secondProblem.sentence import Sentence


class RiddleConstraint(Constraint[Sentence, Sentence]):
    def __init__(self, first_sentence, second_sentence, neighbours=False, left_side_neighbour=None, opposite_sentences=False):
        super().__init__([first_sentence, second_sentence])
        self.first_sentence = first_sentence
        self.second_sentence = second_sentence
        self.neighbours = neighbours
        self.left_side_neighbour = left_side_neighbour
        self.opposite_sentences = opposite_sentences

    def satisfied(self, assignment: Dict[Sentence, House]):
        # jesli sasiedzi to sprawdz czy domy sa obok (numery) ale po co mi to sprawdzac tutaj?
        # jesli to juz sa przypisane
        if not self.opposite_sentences:
            if self.neighbours and self.first_sentence in assignment and self.second_sentence in assignment:
                if self.left_side_neighbour is None:
                    if abs(assignment[self.first_sentence].number - assignment[self.second_sentence].number) != 1:
                        return False
                elif self.left_side_neighbour:
                    if assignment[self.first_sentence].number - assignment[self.second_sentence].number != -1:
                        return False
                else:
                    if assignment[self.first_sentence].number - assignment[self.second_sentence].number != 1:
                        return False

        # czy powtarza sie dom dla takich samych typow (koloru, narodowosci itd)
        for s in assignment:
            for a in assignment:
                if s != a and s.type == a.type:
                    if assignment[s] == assignment[a]:
                        return False

        if self.first_sentence not in assignment or self.second_sentence not in assignment:
            return True

        # sprawdzenie czy pierwsza sentencja dotyczy tego samego domu co druga
        if not self.neighbours and not self.opposite_sentences:
            return assignment[self.first_sentence] == assignment[self.second_sentence]

        return True
