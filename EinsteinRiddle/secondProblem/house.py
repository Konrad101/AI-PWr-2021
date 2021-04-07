class House:
    def __init__(self, number):
        self.number = number
        self.owner = None
        self.color = None
        self.drink = None
        self.smoke = None
        self.animals = None

    def __str__(self):
        return "House " + str(self.number)
