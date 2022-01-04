class User:
    """
    User - class responsibles for basic user which takes part into mini-games
    """

    def __init__(self, nick, level='normal'):
        """Creates exacly user

        Parameters
        ----------
        nick : str
            The nick of the user
        level : str, optional
            The level of difficulty in chosen quiz
        other parameters : int
            Amount of points in each game
        """
        self.nick = nick
        self.level = level

        self.all_points = 0
        self.quiz_points = 0
        self.num_guess_points = 0
        self.card_points = 0
        self.memory_points = 0


    def __call__(self, new_nick):
        """Method that allows to change the nick

        Parameters
        ----------
        new_nick : str
            The user's new nick
        """

        self.nick = new_nick


    def __iadd__(self, amounts_of_points):
        """Method that allows to add points

        Parameters
        ----------
        amounts_of_points : int
            The user's overall amount of points from all games
        """

        self.all_points += amounts_of_points
        return self


    def __str__(self):
        """Method which show all of user's points"""
        print(f'You overall scored: {self.all_points}!')
        print(f'In quiz you scored: {self.quiz_points}')
        print(f'In number guessing game you scored: {self.num_guess_points}')
        print(f'In russian schnapsen game you scored: {self.card_points}')
        print(f'In memory game you scored: {self.memory_points}')
