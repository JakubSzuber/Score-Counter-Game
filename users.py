class User:
    def __init__(self, nick, level='normal'):
        self.nick = nick
        self.level = level
        self.all_points = 0

        self.quiz_points = 0
        self.num_guess_points = 0
        self.card_points = 0
        self.memory_points = 0

    def __call__(self, new_nick):  # Method which allows to change nick
        self.nick = new_nick

    def __iadd__(self, amounts_of_points):  # Method which allows to add points
        self.all_points += amounts_of_points
        return self

    def __str__(self):  # Method which show all of user's points
        print(f'You overall scored: {self.all_points}!')
        print(f'In quiz you scored: {self.quiz_points}')
        print(f'In number guessing game you scored: {self.num_guess_points}')
        print(f'In russian schnapsen game you scored: {self.card_points}')
        print(f'In memory game you scored: {self.memory_points}')
