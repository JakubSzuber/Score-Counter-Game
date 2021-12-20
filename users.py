class User:
    def __init__(self, nick, level):
        self.nick = nick
        self.level = level
        self.points = 0

    def __call__(self, amounts_of_points):
        self.points += amounts_of_points

    @staticmethod
    def todo():
        pass
