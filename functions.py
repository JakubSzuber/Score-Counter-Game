from itertools import chain
from functools import lru_cache
from time import sleep
from contextlib import contextmanager
from datetime import datetime
from time import time
import math
from random import (sample, choice, randint)
from string import (digits, ascii_letters)
from users import User
from player import Player


# Context managers and wrappers:
@contextmanager
def cm_sing_in_window(current_user):
    print('You nick and time of staring playing will be saved into file (and your every activity in this game).')
    sleep(2)
    print('Saving, pleas wait...')
    yield
    with open(r'C:\Users\jszub\OneDrive\Pulpit\test_cm.txt', 'a') as file:
        file.write(f'{current_user.nick} started playing at {datetime.now()}\n')
    print('Saving succesful!')
    sleep(2)
    cleaner()


class CmEndWindow:
    def __init__(self, path, method, current_user):
        self.file_obj = open(path, method)
        self.current_user = current_user

    def __enter__(self):
        print('Saving overall score into file, pleas wait...')
        self.file_obj.write(f'{self.current_user.nick} end with score: {self.current_user.allpoints}\n')
        print('Saving succesful!')
        sleep(2)

    def __exit__(self):
        self.file_obj.close()


def error_handler(func):  # TODO change this name
    def arguments(*args):
        while True:
            try:
                on = func(*args)
            except ValueError as e:
                print('You entered value in wrong type! Details: ', e)
                sleep(4)
            except AssertionError as e:
                print('You entered value in incorrect way! Details: ', e)
                sleep(4)
            except Exception as e:  # TODO add more excetions
                print('Appeared unexpected error, try again. Details: ', e)
                sleep(4)
            else:
                break
        return on
    return arguments



def minigame_wrapper(game_type):
    def take_clas(function):
        def wrapper(*args):
            with open(r'C:\Users\jszub\OneDrive\Pulpit\test_cm.txt', 'a') as file:
                file.write(f'User start playing {game_type} at {datetime.now()}\n')
                start = time()
                on = function(*args)
                end = time()
                file.write(f'User end playing {game_type} at {datetime.now()} (about {round(end-start)} seconds in game)\n')
            return on
        return wrapper
    return take_clas



# General functions:
def start_window():
    print('Hello user!')
    print('You will be playing in few games, where you can completing tasks and collecting points. \nWhen you end all four minigames you could see leader board and start playing anew. Good luck!\n')
    print('PS: Follow the guidelines carefully because if you cause an error you will have to play mini-game from the begining!')
    sleep(4)
    cleaner()
    print('Here is the list of games that you will play sequentially:')
    print('1 - quizzes about path or python.')
    print('2 - number guessing game.')
    print('3 - russian schnapsen game (card game).')
    print('4 - color-number memory game.')
    #print('Enter 0 to open pause menu.')  # TODO to create this window is required npyscreen (a Python curses wrapper)
    print('-'*20)
    input('If you ready enter anything: ')


@error_handler
def sing_in_window(l_board):
    print('Before we start enter data:')
    user_nick = input('Your nick: ')

    assert user_nick not in l_board

    print('\nChose level of difficult in quiz:\n-normal\n-medium')
    diff_level = input('Your answer: ')

    assert diff_level == ('normal' or 'medium')

    curr_us = User(user_nick, diff_level)
    cleaner()
    return curr_us


def end_window_1(user_class):
    print(painter(f'Congratulations {user_class.nick}!', g=255, b=100))
    print(user_class)


'''
def pause_menu_window():
    print(10*'-', 'Pause menu', 10*'-')
    print(painter('Enter 1 to see how much time have you playing', 192, 192, 192))
    print(painter('Enter 2 to see how much points have you scored', 192, 192, 192))
    print(painter('Enter 3 to end game', 192, 192, 192))
    print(painter('-'*20, 192, 192, 192))
'''  # TODO to create this window is required npyscreen (a Python curses wrapper)



# Minigames applications:
@error_handler
@minigame_wrapper('quiz')
def quiz(user_class):
    print(painter('-------We can start quiz now!-------', g=255, b=100))
    print('Choose what topic of the quiz you prefer: python or math?')
    quiz_topic = input('Your answer: ')
    cleaner()

    match user_class.level:

        case 'medium':
            print('You chose medium difficulty, you can get 150 points for the right answer!')
            if quiz_topic == 'python':
                print(painter('Your answer shulod be correct to examplepattern: a\n', r=200))
                sleep(3)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_medium_quiz', 'r') as file:  # Here use absolute path of the file where you have file with content of teh quiz
                    quiz_body(user_class, file, 'python')
            else:
                print(painter('Your answer shulod be correct to examplepattern: 2\n', r=200))
                sleep(3)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_medium_quiz', 'r') as file:
                    quiz_body(user_class, file, 'math')

        case 'normal':
            print('You chose normal difficulty, you can get 100 points for the right answer!')
            if quiz_topic == 'python':
                print(painter('Your answer shulod be correct to examplepattern: a\n', r=200))
                sleep(3)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_normal_quiz', 'r') as file:
                    quiz_body(user_class, file, 'python')
            else:
                print(painter('Your answer shulod be correct to examplepattern: 2\n', r=200))
                sleep(3)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_normal_quiz', 'r') as file:
                    quiz_body(user_class, file, 'math')


@error_handler
@minigame_wrapper('number guessing')
def number_guessing(user_class):
    print(painter('-------We can start number guessing game now!-------', g=255, b=100))
    print(painter('Below rules of the game:', 255))
    print(painter('-You will choose range of the number to quess one number from this range', 255))
    print(painter('-The lowest possible number is 0', 255))
    print(painter('-You have no limit of trials untill you quess the number', 255))
    print(painter('-Program will help you to guess it', 255))
    print(painter('-Remember the larger the range you choose and the faster you guess the number, the more points you get!\n', 255))

    choosen_range = int(input('If you read rules you can choose the range of the possible numbers: '))
    print('Finally we can start game!')
    sleep(2)
    cleaner()

    drawn_num = randint(0, choosen_range)
    counter = 0

    user_trial = int(input('Guess number: '))
    counter += 1

    while user_trial != drawn_num:
        if user_trial < drawn_num:
            print('Too small number!')
            user_trial = int(input('Guess number: '))
            counter += 1
        elif user_trial > drawn_num:
            print('Too big number!')
            user_trial = int(input('Guess number: '))
            counter += 1
    else:
        earned_points = choosen_range//counter
        user_class += earned_points
        user_class.num_guess_points += earned_points
        print(painter(f'Gangratulations {user_class.nick}, you quess correct after {counter} times!', g=255))
        print(painter(f'You earned {earned_points} points', g=255))


@error_handler
@minigame_wrapper('russian schnapsen game')
def russian_schnapsen_game(user_class):
    print(painter('-------We can start card game now!-------', g=255, b=100))
    print(painter('Below rules of the game:', 255))
    print(painter('-You will play against computer', 255))
    print(painter('-Game is absolutely random', 255))
    print(painter('-You have 12 cards in your deck', 255))
    print(painter('-If your card have bigger value than your rival\'s card you earn sum of points from both cards in a turn', 255))
    print(painter('-If you have king and queen from one fit you can get up to 100 points!\n', 255))

    input('If you ready enter anything: ')
    print('Finally we can start game!')
    sleep(2)
    cleaner()

    suit = ['heart', 'tile', 'clover', 'piker']
    figures = ['9', '10', 'jack', 'queen', 'king', 'ace']

    deck_parts = Player.player_creator(suit, figures, user_class.nick, user_class.level)
    player_01 = deck_parts[0]
    player_02 = deck_parts[1]

    player_02.nick = 'Computer'

    player_01.report_marriage()
    player_02.report_marriage()

    player_01_cards = player_01.card_generator()
    player_02_cards = player_02.card_generator()

    while True:
        try:
            card_1 = next(player_01_cards)
            card_2 = next(player_02_cards)

            print(f'{user_class.nick} card: {card_1}')
            print(f'Computer card: {card_2}')

            card_1_power = list(card_1.values())[0]
            card_2_power = list(card_2.values())[0]

            if card_1_power > card_2_power:
                print(painter(f'{user_class.nick} is winning this turn!', g=255))
                player_01.all_points += card_1_power+card_2_power
                player_01.card_points += card_1_power + card_2_power
                user_class += card_1_power+card_2_power
                user_class.card_points += card_1_power+card_2_power
                sleep(2)
                cleaner()
            elif card_1_power == card_2_power:
                player_02.all_points += card_1_power+card_2_power
                player_02.card_points += card_1_power + card_2_power
                print('Draw!')
                sleep(2)
                cleaner()
            else:
                print(painter(f'Computer\'s winning this turn!', 255))
                user_class += card_1_power + card_2_power
                user_class.card_points += card_1_power + card_2_power
                sleep(2)
                cleaner()
        except StopIteration:
            print(f'{player_01.nick}, you\'ve earn {player_01.card_points} points')
            print(f'Computer, earn {player_02.card_points} points')
            print(f'Winner is: {player_01.nick}!' if player_01.card_points > player_02.card_points else f'Winner is: computer!')
            print('Computer: ', end='')
            player_02.ending()
            break

    user_class.all_points += player_01.all_points
    user_class.card_points += player_01.all_points


@error_handler
@minigame_wrapper('memory game')
def memory_game(user_class):
    print(painter('We can start memory game now!', g=255, b=100))
    print(painter('Below rules of the first part of game:', 255))
    print(painter('-You will see number for 2 second and then you have to enter it correct', 200))
    print(painter('-The amount of the digits in the number will be increasing', 200))
    print(painter('-If you make a mistake the first part of the game will end', 200))
    print(painter('-You can earn more points from the bigger numbers!', 200))

    input('If you\'re ready enter anything: ')
    print('Finally we can start game!')
    sleep(2)
    cleaner()

    iterator = 100
    while True:
        print('Number:', secret_num := randint(iterator, iterator*2))
        sleep(3)
        cleaner()

        users_trial = int(input('Enter number: '))

        if users_trial == secret_num:
            print(painter(f'Correct answer! You get {iterator//20} points!', g=255))
            user_class.all_points += iterator//20
            user_class.memory_points += iterator//20
            sleep(2)
            cleaner()
        else:
            print(painter('Sorry bad answer! First part of game is over!', 255))
            sleep(2)
            cleaner()
            cleaner()
            break

        iterator *= 10


    print(painter('Below rules of the second part of game:', 255))
    print(painter('-You will se random password in the random color for 2 seconds, after that you have to enter it and its color', 200))
    print(painter('-The length of the password will be increasing', 200))
    print(painter('-For guessing the password correctly you get 100 points for guessing the color 50', 200))
    print(painter('-If you make a mistake the game will end', 200))

    input('If you\'re ready enter anything: ')
    print('Finally we can start game!')
    sleep(2)
    cleaner()

    colors = ['red', 'green', 'blue', 'pink']
    chars_num = list(chain(digits, ascii_letters))
    counter = 2

    while True:
        if counter == 60:
            print('Incredible score! You\'ve got maximum points form part two!')
            break

        gen_password = sample(chars_num, counter)
        gen_color = choice(colors)

        match gen_color:
            case 'red':
                combination = [255, 0, 0]
            case 'green':
                combination = [0, 255, 0]
            case 'blue':
                combination = [0, 50, 200]
            case 'pink':
                combination = [255, 0, 255]

        print(painter(''.join(gen_password), r=combination[0],  g=combination[1], b=combination[2],))
        sleep(3)
        cleaner()

        user_password_answer = input('Enter password: ')
        if ''.join(gen_password) == user_password_answer:
            print(painter('Correct answer you\'re getting points!', g=255))
            user_class.all_points += 100
            user_class.memory_points += 100
        else:
            print(painter('Sorry bad answer! Second part of game is over!', 255))
            break

        user_color_answer = input('Enter the color of teh password: ')
        if gen_color == user_color_answer:
            print(painter('Correct answer you\'re getting points!', g=255))
            sleep(2)
            user_class.all_points += 50
            user_class.memory_points += 50
        else:
            print(painter('Sorry bad answer! Second part of game is over!', 255))
            break

        cleaner()
        counter += 1



# Auxiliary functions and temporary function:
def cleaner():  # TODO change this function into npyscreen (a Python curses wrapper) in the future
    print(20*'\n')


@error_handler
@lru_cache
def quiz_body(us_cl, f, quiz_type):
    cleaner()
    counter = 0
    correct_answers = 0
    for line in f:
        counter += 1

        if counter % 6 == 0:
            user_answer = input('Your answer: ')
            if quiz_type == 'math':
                correct_ans = eval(line.rstrip())
                if float(user_answer) == correct_ans:
                    print('Good answer, you\'re getting points!')
                    us_cl += 150  # Use mothod call in class User (add points to object)
                    us_cl.quiz_points += 150
                    sleep(2)
                    cleaner()
                else:
                    print('Bad answer!')
                    sleep(2)
                    cleaner()
            else:
                correct_ans = line.rstrip()
                if user_answer == correct_ans:
                    print('Good answer, you\'re getting points!')
                    us_cl += 150  # Use mothod call in class User (add points to object)
                    us_cl.quiz_points += 150
                    correct_answers += 1
                    sleep(2)
                    cleaner()
                else:
                    print('Bad answer!')
                    sleep(2)
                    cleaner()
        else:
            print(line.rstrip())

    print(f'Congratulations {us_cl.nick} you finished quiz with score {correct_answers}/10, that gives us: {us_cl.quiz_points} points!')


def painter(text, r=0, g=0, b=0):
    return f'\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m'
