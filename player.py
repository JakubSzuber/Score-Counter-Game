from random import shuffle
from time import sleep

from users import User


class Player(User):
    """
    Player - class responsibles for user which takes part into card game
    """

    def __init__(self, deck, nick):
        """Creates user which plays only in card game

        Parameters
        ----------
        deck : list
            The player's cards
        nick : str
            The nick of the player
        """
        self.deck = deck
        super().__init__(nick)


    def card_generator(self):
        """Method that return next card from palyer's deck"""
        for i in range(len(self.deck)):
            yield self.deck[i]
        else:
            print('All cards were given!')


    def report_marriage(self):
        """Method that checks if player has got marriage in its deck and possibly report that"""
        if {('clover', 'queen'): 12} in self.deck:
            if {('clover', 'king'): 13} in self.deck:
                print(f'{self.nick} have clover marriage and getting 60 points!\n')
                sleep(2)
                self.all_points += 60
                self.card_points += 60
        if {('tile', 'queen'): 12} in self.deck:
            if {('tile', 'king'): 13} in self.deck:
                print(f'{self.nick} have tile marriage and getting 80 points!\n')
                sleep(2)
                self.all_points += 80
                self.card_points += 80
        if {('piker', 'queen'): 12} in self.deck:
            if {('piker', 'king'): 13} in self.deck:
                print(f'{self.nick} have piker marriage and getting 40 points!\n')
                sleep(2)
                self.all_points += 40
                self.card_points += 40
        if {('heart', 'queen'): 12} in self.deck:
            if {('heart', 'king'): 13} in self.deck:
                print(f'{self.nick} have heart marriage and getting 100 points!\n')
                sleep(2)
                self.all_points += 100
                self.card_points += 100


    @classmethod
    def player_creator(cls, suit, figures, nick):
        """Method that creates two players and returns decks for each of them

        Parameters
        ----------
        suit : list
            All types card's suit
        figures : list
            All types card's figure
        nick : str
            The user's nick

        Returns
        -------
        list
            a list which have ready decks (shuffled) for both player which take part into the game
        """
        dict_all_cards = {}
        all_cards_list = []

        for s in suit:
            power = (i for i in range(9, 15))
            for f in figures:
                dict_all_cards[(s, f)] = next(power)

        for i in dict_all_cards:
            all_cards_list.append({i: dict_all_cards[i]})

        shuffle(all_cards_list)

        player_1 = cls(all_cards_list[:12], nick)
        player_2 = cls(all_cards_list[12:], nick)

        return [player_1, player_2]


    ending = staticmethod(lambda: print('Thanks for playing, good game!'))
    """Method which prints farewell"""
