from random import shuffle
from time import sleep

from users import User


class Player(User):
    def __init__(self, deck, nick, level='normal'):
        self.deck = deck
        super().__init__(nick, level)

    def card_generator(self):  # Generator which return next card from deck
        for i in range(len(self.deck)):
            yield self.deck[i]
        else:
            print('All cards were given!')

    def report_marriage(self):  # Method which inform about marriage
        clover = 0
        tile = 0
        piker = 0
        heart = 0
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
            print(f'{self.nick} have clover marriage and getting 60 pomits!\n')
            sleep(2)
            self.points += 60
        if tile == 2:
            print(f'{self.nick} have tile marriage and getting 80 pomits!\n')
            sleep(2)
            self.points += 80
        if heart == 2:
            print(f'{self.nick} have heart marriage and getting 100 pomits!\n')
            sleep(2)
            self.points += 100
        if piker == 2:
            print(f'{self.nick} have piker marriage and getting 40 pomits!\n')
            sleep(2)
            self.points += 40

    @classmethod
    def player_creator(cls, suit, figures, nick, level):  # method which create instance
        dict_all_cards = {}
        all_cards_list = []

        for s in suit:
            power = (i for i in range(9, 15))
            for f in figures:
                dict_all_cards[(s, f)] = next(power)

        for i in dict_all_cards:
            all_cards_list.append({i: dict_all_cards[i]})

        shuffle(all_cards_list)

        player_1 = cls(all_cards_list[:12], nick, level)
        player_2 = cls(all_cards_list[12:], nick, level)

        return [player_1, player_2]

    ending = staticmethod(lambda: print('Thanks for playing, good game!'))

    # TODO set some attributes to private
    # TODO create here property (in any way) which print amount of points etc.
