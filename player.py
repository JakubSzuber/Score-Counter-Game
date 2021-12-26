import itertools  # todo do not import whole module
import random

from users import User


class Player(User):
    def __init__(self, deck, nick, level='normal'):
        self.deck = deck
        super().__init__(nick, level)

    # todo meybe add here decorator
    def give_card(self):  # Generator which return next card from deck
        pass

    # todo meybe add here decorator
    def report_marriage(self):  # Method which inform about marriage
        pass

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

        random.shuffle(all_cards_list)

        player_1 = cls(all_cards_list[:12], nick, level)
        player_2 = cls(all_cards_list[:12], nick, level)

        return [player_1, player_2]

    ending = staticmethod(lambda: print('Good game!'))

    # TODO set some attributes to private
    # TODO create here property (in any way) which print amount of points etc.
