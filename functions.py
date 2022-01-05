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
    with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\logs.txt', 'a') as file:
        file.write(f'{current_user.nick} started playing at {datetime.now()}\n')
    print('Saving succesful!')
    sleep(2)
    cleaner()


class CmEndWindow:
    def __init__(self, path, method, current_user):
        self.file_obj = open(path, method)
        self.current_user = current_user

    def __enter__(self):
        print('This is and of the application!')
        print('Saving overall score into file, pleas wait...')
        self.file_obj.write(f'{self.current_user.nick} end with score: {self.current_user.all_points}\n\n')
        print('Saving succesful!')
        sleep(2)
        cleaner()

    def __exit__(self, type, value, traceback):
        self.file_obj.close()


def error_handler(func):
    def arguments(*args):
        while True:
            try:
                cleaner()
                on = func(*args)
            except ValueError as e:
                print(painter('You entered wrong type of the value!', 250))
                print('Details:', e)
                sleep(5)
            except AssertionError as e:
                print(painter('A logic of the program has broken!', 250))
                print('Details:', e)
                sleep(5)
            except Exception as e:
                print(painter('Appeared unexpected error!', 250))
                print('Details:', e)
                sleep(5)
            else:
                break
        return on
    return arguments



def minigame_wrapper(game_type):
    def take_clas(function):
        def wrapper(*args):
            with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\logs.txt', 'a') as file:
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
    # print('Enter 0 to open pause menu.')  # TODO to create this window is required npyscreen (a Python curses wrapper)
    print('-'*58)
    input('If you ready enter anything: ')


@error_handler
def sing_in_window(l_board):
    print('Before we start enter data:')
    user_nick = input('Your nick: ')

    assert user_nick not in l_board, 'User with this nick is already saved in the leader board!'
    assert user_nick != '', 'Your nick must have characters!'

    print('\nChose level of difficult in quiz:\n-normal\n-medium')
    diff_level = input('Your answer: ')

    assert diff_level != 'normal' or 'medium', 'You entered wrong level of the difficulty (typo)!'

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
    assert quiz_topic == 'python' or 'math', 'You entered wrong type of the quiz (typo)!'

    cleaner()

    match user_class.level:
        case 'medium':
            print('You chose medium difficulty, you can get 150 points for the right answer!')
            if quiz_topic == 'python':
                print(painter('Your answer shoulod be correct to examplepattern: a\n', r=250))
                sleep(4)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_medium_quiz', 'r') as file:  # Used absolute path of the file where is content of the quiz
                    quiz_body(user_class, file, 'python')
            else:
                print(painter('Your answer shoulod be correct to examplepattern: 2\n', r=250))
                sleep(4)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_medium_quiz', 'r') as file:
                    quiz_body(user_class, file, 'math')
        case 'normal':
            print('You chose normal difficulty, you can get 100 points for the right answer!')
            if quiz_topic == 'python':
                print(painter('Your answer shoulod be correct to examplepattern: a\n', r=250))
                sleep(4)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_normal_quiz', 'r') as file:
                    quiz_body(user_class, file, 'python')
            else:
                print(painter('Your answer shoulod be correct to examplepattern: 2\n', r=250))
                sleep(4)
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
    assert choosen_range >= 2, 'You chosen to small range of the numbers'
    print('Finally we can start game!')
    sleep(2)
    cleaner()

    drawn_num = randint(0, choosen_range)
    counter = 0

    user_trial = int(input('Guess number: '))
    counter += 1

    while user_trial != drawn_num:
        if user_trial < drawn_num:
            print('Too small number!\n')
            user_trial = int(input('Guess number: '))
            counter += 1
        elif user_trial > drawn_num:
            print('Too big number!\n')
            user_trial = int(input('Guess number: '))
            counter += 1
    else:
        earned_points = choosen_range//counter*10
        user_class += earned_points
        user_class.num_guess_points += earned_points
        print(painter(f'Gangratulations {user_class.nick}, you quess correct after {counter} times!', g=255))
        print(painter(f'You earned {earned_points} points', g=255))
        sleep(3)


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

    deck_parts = Player.player_creator(suit, figures, user_class.nick)
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
            print(f'Computer, earn {player_02.card_points} points\n')
            print(f'Winner is: {player_01.nick}!!!' if player_01.card_points > player_02.card_points else f'Winner is: computer!')
            print('Computer: ', end='')
            player_02.ending()
            sleep(4.5)
            break

    user_class.all_points += player_01.all_points
    user_class.card_points += player_01.all_points


@error_handler
@minigame_wrapper('memory game')
def memory_game(user_class):
    print(painter('We can start memory game now!', g=255, b=100))
    print(painter('Below rules of the first part of game:', 255))
    print(painter('-You will see number for 2 second and then you have to enter it correct', 255))
    print(painter('-The amount of the digits in the number will be increasing', 255))
    print(painter('-If you make a mistake the first part of the game will end', 255))
    print(painter('-You can earn more points from the bigger numbers!', 255))

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
    print(painter('-You will se random password in the random color for 2 seconds, after that you have to enter it and its color', 255))
    print(painter('-The length of the password will be increasing', 255))
    print(painter('-For guessing the password correctly you get 100 points for guessing the color 50', 255))
    print(painter('-Possible color answers: pink, red, blue, green', 255))
    print(painter('-If you make a mistake the game will end', 255))

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
                combination = [30, 144, 255]
            case 'pink':
                combination = [255, 0, 255]

        print(painter(''.join(gen_password), r=combination[0],  g=combination[1], b=combination[2]))
        sleep(3)
        cleaner()

        user_password_answer = input('Enter password: ')
        assert user_password_answer != '', 'Password must contains characters'

        if ''.join(gen_password) == user_password_answer:
            print(painter('Correct answer you\'re getting points!', g=255))
            user_class.all_points += 100
            user_class.memory_points += 100
        else:
            print(painter('Sorry bad answer! Second part of game is over!', 255))
            break

        user_color_answer = input('Enter the color of the password: ')
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
            assert user_answer != '', 'You didn\'t select any answer!'
            if quiz_type == 'math':
                correct_ans = eval(line.rstrip())
                if float(user_answer) == correct_ans:
                    print(painter('Good answer, you\'re getting points!', g=255))
                    us_cl += 150  # Use mothod call in class User (add points to object)
                    us_cl.quiz_points += 150
                    correct_answers += 1
                    sleep(2)
                    cleaner()
                else:
                    print(painter('Bad answer!', 255))
                    sleep(2)
                    cleaner()
            else:
                correct_ans = line.rstrip()
                if user_answer == correct_ans:
                    print(painter('Good answer, you\'re getting points!', g=255))
                    us_cl += 150  # Use mothod call in class User (add points to object)
                    us_cl.quiz_points += 150
                    correct_answers += 1
                    sleep(2)
                    cleaner()
                else:
                    print(painter('Bad answer!', 255))
                    sleep(2)
                    cleaner()
        else:
            print(line.rstrip())

    print(f'Congratulations {us_cl.nick} you finished quiz with score {correct_answers}/10, that gives us: {us_cl.quiz_points} points!')
    sleep(3)


def painter(text, r=0, g=0, b=0):
    return f'\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m'
