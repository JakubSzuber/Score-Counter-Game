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
        clover = 0
        tile = 0
        piker = 0
        heart = 0
        '''
        for dictionary in self.deck:
            if ('clover', 'queen') in dictionary.keys():
                clover += 1
            if ('clover', 'king') in dictionary.keys():
                clover += 1
            if ('tile', 'queen') in dictionary.keys():
                tile += 1
            if ('tile', 'king') in dictionary.keys():
                tile += 1
            if ('piker', 'queen') in dictionary.keys():
                piker += 1
            if ('piker', 'king') in dictionary.keys():
                piker += 1
            if ('heart', 'queen') in dictionary.keys():
                heart += 1
            if ('heart', 'king') in dictionary.keys():
                heart += 1

        if clover == 2:
            print(f'{self.nick} have clover marriage and getting 60 points!\n')
            sleep(2)
            self.all_points += 60
        if tile == 2:
            print(f'{self.nick} have tile marriage and getting 80 points!\n')
            sleep(2)
            self.all_points += 80
        if heart == 2:
            print(f'{self.nick} have heart marriage and getting 100 points!\n')
            sleep(2)
            self.all_points += 100
        if piker == 2:
            print(f'{self.nick} have piker marriage and getting 40 points!\n')
            sleep(2)
            self.all_points += 40
        '''  # TODO if code won't work uncomment old version of this method
        for dictionary in self.deck:
            if ('clover', 'queen') and ('clover', 'king') in dictionary.keys():
                print(f'{self.nick} have clover marriage and getting 60 points!\n')
                sleep(2)
                self.all_points += 60
            if ('tile', 'queen') and ('tile', 'king') in dictionary.keys():
                print(f'{self.nick} have tile marriage and getting 80 points!\n')
                sleep(2)
                self.all_points += 80
            if ('piker', 'queen') and ('piker', 'king') in dictionary.keys():
                print(f'{self.nick} have piker marriage and getting 40 points!\n')
                sleep(2)
                self.all_points += 40
            if ('heart', 'queen') and ('heart', 'king') in dictionary.keys():
                print(f'{self.nick} have heart marriage and getting 100 points!\n')
                sleep(2)
                self.all_points += 100


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
        power = (i for i in range(9, 15))

        for s in suit:
            for f in figures:
                dict_all_cards[(s, f)] = next(power)

        for i in dict_all_cards:
            all_cards_list.append({i: dict_all_cards[i]})

        shuffle(all_cards_list)

        player_1 = cls(all_cards_list[:12], nick)
        player_2 = cls(all_cards_list[12:], nick)

        return [player_1, player_2]


    ending = staticmethod(lambda: print('Thanks for playing, good game!'))  # Method which prints farewell
