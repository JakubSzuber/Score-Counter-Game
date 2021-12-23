class User:
    def __init__(self, nick, level='normal'):
        self.nick = nick
        self.level = level
        self.points = 0

    def __call__(self, new_nick):  # Method which allows to change nick
        self.nick = new_nick

    def __iadd__(self, amounts_of_points):  # Method which allows to add points
        self.points += amounts_of_points
        return self

    def __str__(self):
        print(f'User {self.nick} for now have: {self.points} points')

    @staticmethod
    def todo():
        pass
