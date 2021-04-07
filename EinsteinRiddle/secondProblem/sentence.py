class Sentence:
    def __init__(self, sentence_type, value):
        self.type = sentence_type
        self.value = value

    def __str__(self):
        return self.type + ' ' + self.value
