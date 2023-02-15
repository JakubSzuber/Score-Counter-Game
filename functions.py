from itertools import chain
from functools import lru_cache
from time import sleep
from contextlib import contextmanager
from datetime import datetime
from time import time
import math
from typing import TextIO, Generator, Callable
from random import (sample, choice, randint)
from string import (digits, ascii_letters)
from users import User
from player import Player


# Global variable which counts the user's correct answers
correct_answers: list[int] = []

# Context managers and wrappers:
@contextmanager
def cm_sign_in_window(current_user: User) -> None:
    print('Your nick and time of staring playing will be saved into file (and your every activity in this game).')
    sleep(3.5)
    print('Saving, pleas wait...')
    yield
    with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\logs.txt', 'a') as file:  # Used absolute path of the file in which are stored logs from app
        file.write(f'\n{current_user.nick} started playing at {datetime.now()}\n')
    print('Saving succesful!')
    sleep(2)
    cleaner()


class CmEndWindow:
    def __init__(self, path: str, method: str, current_user: User) -> None:
        self.file_obj: TextIO = open(path, method)
        self.current_user: User = current_user

    def __enter__(self) -> None:
        correct_answers.clear()
        print('This is end of the application!')
        print('Saving overall score into file, pleas wait...')
        self.file_obj.write(f'{self.current_user.nick} end with score: {self.current_user.all_points}\n')
        print('Saving succesful!')
        sleep(4)
        cleaner()

    def __exit__(self, exc_type: str, exc_val: str, exc_tb: str) -> None:
        self.file_obj.close()


def error_handler(func: Callable):
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
            except (FileNotFoundError, FileExistsError) as e:
                print(painter('Appeared error with file path!', 250))
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


def minigame_wrapper(game_type: str):
    def take_clas(function: Callable):
        def wrapper(*args):
            with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\logs.txt', 'a') as file:
                file.write(f'User start playing {game_type} at {datetime.now()}\n')
                start: float = time()
                on = function(*args)
                end: float = time()
                file.write(f'User end playing {game_type} at {datetime.now()} (about {round(end-start)} seconds in game)\n')
            return on
        return wrapper
    return take_clas


# General functions:
def start_window() -> None:
    print('Hello user!')
    print('You will be playing in few games, where you can completing tasks and collecting points. \nWhen you end all four minigames you could see leader board and start playing anew. Good luck!\n')
    print('PS: Follow the guidelines carefully because if you cause an error you probably will have to play mini-game from the begining!')
    sleep(12)
    cleaner()
    print('Here is the list of games that you will play sequentially:')
    print('1 - quizzes about math or python.')
    print('2 - number guessing game.')
    print('3 - russian schnapsen game (card game).')
    print('4 - color-number memory game.')
    print('-'*58)
    input('If you ready enter anything: ')


@error_handler
def sign_in_window(l_board: list[int, dict[str, int]]) -> User:
    print('Before we start enter data:')
    user_nick: str = input('Your nick: ')

    assert user_nick not in l_board, 'User with this nick is already saved in the leader board!'
    assert user_nick != '', 'Your nick must have characters!'

    print('\nChose level of difficult in quiz:\n-normal\n-medium')
    diff_level: str = input('Your answer: ')

    assert diff_level == 'normal' or 'medium', 'You entered wrong level of the difficulty (typo)!'

    curr_us: User = User(user_nick, diff_level)
    cleaner()
    return curr_us


def end_window_1(user_class: User) -> None:
    print(painter(f'Congratulations {user_class.nick}!', g=255, b=100))
    print(user_class)


# Minigames applications:
@error_handler
@minigame_wrapper('quiz')
def quiz(user_class: User) -> None:
    print(painter('-------We can start quiz now!-------', g=255, b=100))
    print('Choose what topic of the quiz you prefer: python or math?')
    quiz_topic: str = input('Your answer: ')
    assert quiz_topic == 'python' or 'math', 'You entered wrong type of the quiz (typo)!'

    cleaner()

    match user_class.level:
        case 'medium':
            print('You chose medium difficulty, you can get 150 points for the right answer!')
            if quiz_topic == 'python':
                print(painter('Your answer should be correct to example pattern: a\n', r=250))
                sleep(5)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_medium_quiz', 'r') as file:  # Used absolute path of the file where is content of the quiz
                    quiz_body(user_class, file, 'python')
            else:
                print(painter('Your answer should be correct to example pattern: 2\n', r=250))
                sleep(5)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_medium_quiz', 'r') as file:
                    quiz_body(user_class, file, 'math')
        case 'normal':
            print('You chose normal difficulty, you can get 100 points for the right answer!')
            if quiz_topic == 'python':
                print(painter('Your answer should be correct to example pattern: a\n', r=250))
                sleep(5)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_normal_quiz', 'r') as file:
                    quiz_body(user_class, file, 'python')
            else:
                print(painter('Your answer should be correct to example pattern: 2\n', r=250))
                sleep(5)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_normal_quiz', 'r') as file:
                    quiz_body(user_class, file, 'math')


@error_handler
@minigame_wrapper('number guessing')
def number_guessing(user_class: User) -> None:
    print(painter('-------We can start number guessing game now!-------', g=255, b=100))
    print(painter('Below rules of the game:', 255))
    print(painter('-You will choose range of the number to quess one number from this range', 255))
    print(painter('-The lowest possible number is 0', 255))
    print(painter('-You have no limit of trials untill you quess the number', 255))
    print(painter('-Program will help you to guess it', 255))
    print(painter('-Remember the larger the range you choose and the faster you guess the number, the more points you get!', 255))
    print(painter('-Your answer should be correct to example pattern: 35\n', r=250))

    choosen_range: int = int(input('If you read rules you can choose the range of the possible numbers (e.g. 100): '))
    assert choosen_range >= 2, 'You chosen to small range of the numbers'
    print('Finally we can start game!')
    sleep(2)
    cleaner()

    drawn_num: int = randint(0, choosen_range)
    counter: int = 0

    user_trial: int = int(input('Guess number: '))
    counter += 1

    while user_trial != drawn_num:
        if user_trial < drawn_num:
            print('Too small number!\n')
            user_trial: int = int(input('Guess number: '))
            counter += 1
        elif user_trial > drawn_num:
            print('Too big number!\n')
            user_trial: int = int(input('Guess number: '))
            counter += 1
    else:
        earned_points: int = choosen_range//counter*10
        user_class += earned_points
        user_class.num_guess_points += earned_points
        print(painter(f'Congratulations {user_class.nick}, you quess correct after {counter} times!', g=255))
        print(painter(f'You earned {earned_points} points', g=255))
        sleep(3.5)
        cleaner()


@error_handler
@minigame_wrapper('russian schnapsen game')
def russian_schnapsen_game(user_class: User) -> None:
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

    suit: list[str] = ['heart', 'tile', 'clover', 'piker']
    figures: list[str] = ['9', '10', 'jack', 'queen', 'king', 'ace']

    deck_parts: list[Player, Player] = Player.player_creator(suit, figures, user_class.nick)
    player_01: Player = deck_parts[0]
    player_02: Player = deck_parts[1]

    player_02.nick = 'Computer'

    player_01.report_marriage()
    player_02.report_marriage()

    player_01_cards: Generator[dict, None, None] = player_01.card_generator()
    player_02_cards: Generator[dict, None, None] = player_02.card_generator()

    while True:
        try:
            card_1: dict[str, str] = next(player_01_cards)
            card_2: dict[str, str] = next(player_02_cards)

            print(f'{user_class.nick} card: {card_1}')
            print(f'Computer card: {card_2}')

            card_1_power: int = int(list(card_1.values())[0])
            card_2_power: int = int(list(card_2.values())[0])

            if card_1_power > card_2_power:
                print(painter(f'{user_class.nick} is winning this turn!', g=255))
                player_01 += card_1_power+card_2_power
                player_01.card_points += card_1_power + card_2_power
                sleep(2)
                cleaner()
            elif card_1_power == card_2_power:
                player_01 += card_1_power+card_2_power
                player_01.card_points += card_1_power + card_2_power
                player_02 += card_1_power+card_2_power
                player_02.card_points += card_1_power + card_2_power
                print('Draw!')
                sleep(2)
                cleaner()
            else:
                print(painter(f'{player_02.nick} is winning this turn!', r=255))
                player_02 += card_1_power+card_2_power
                player_02.card_points += card_1_power + card_2_power
                sleep(2)
                cleaner()
        except StopIteration:
            print(f'{player_01.nick}, you\'ve earn {player_01.card_points} points')
            print(f'Computer, earn {player_02.card_points} points\n')
            print(f'Winner is: {player_01.nick}!!!' if player_01.card_points > player_02.card_points else f'Winner is: computer!')
            print('Computer: ', end='')
            player_02.ending()
            sleep(6)
            break

    user_class += player_01.all_points
    user_class.card_points += player_01.all_points


@error_handler
@minigame_wrapper('memory game')
def memory_game(user_class: User) -> None:
    print(painter('We can start memory game now!', g=255, b=100))
    print(painter('Below rules of the first part of game:', 255))
    print(painter('-You will see number for 2 second and then you have to enter it correct', 255))
    print(painter('-The amount of the digits in the number will be increasing', 255))
    print(painter('-If you make a mistake the first part of the game will end', 255))
    print(painter('-You can earn more points from the bigger numbers!', 255))
    print(painter('-Your answer should be correct to example pattern: 35\n', r=250))

    input('If you\'re ready enter anything: ')
    print('Finally we can start game!')
    sleep(2)
    cleaner()

    iterator: int = 100
    while True:
        print('Number:', secret_num := randint(iterator, iterator*2))
        sleep(3)
        cleaner()

        users_trial: int = int(input('Enter number: '))

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

    colors: list[str] = ['red', 'green', 'blue', 'pink']
    chars_num: list[str] = list(chain(digits, ascii_letters))
    counter: int = 2

    while True:
        if counter == 60:
            print('Incredible score! You\'ve got maximum points from part two!')
            break

        gen_password: list[str] = sample(chars_num, counter)
        gen_color: str = choice(colors)

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

        user_password_answer: str = input('Enter password: ')
        assert user_password_answer != '', 'Password must contains characters'

        if ''.join(gen_password) == user_password_answer:
            print(painter('Correct answer you\'re getting points!', g=255))
            user_class += 100
            user_class.memory_points += 100
        else:
            print(painter('Sorry bad answer! Second part of game is over!', 255))
            sleep(3)
            cleaner()
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
def cleaner() -> None:  # TODO this function won't be needed when the GUI will be created
    print(20*'\n')


@error_handler
@lru_cache
def quiz_body(us_cl: User, f: TextIO, quiz_type: str) -> None:  # Argument "f" is a file reference
    cleaner()
    counter: int = 0

    for line in f:
        counter += 1

        if counter % 6 == 0:
            user_answer: str = input('Your answer: ')
            assert user_answer != '', 'You didn\'t select any answer!'
            if quiz_type == 'math':
                correct_ans = eval(line.rstrip())
                if float(user_answer) == correct_ans:
                    print(painter('Good answer, you\'re getting points!', g=255))
                    us_cl += 150  # Use method __iadd__() in class User (add points to object)
                    us_cl.quiz_points += 150
                    correct_answers.append(1)
                    sleep(2)
                    cleaner()
                else:
                    print(painter('Bad answer!', 255))
                    correct_answers.append(0)
                    sleep(2)
                    cleaner()
            else:
                correct_ans = line.rstrip()
                if user_answer == correct_ans:
                    print(painter('Good answer, you\'re getting points!', g=255))
                    us_cl += 150
                    us_cl.quiz_points += 150
                    correct_answers.append(1)
                    sleep(2)
                    cleaner()
                else:
                    print(painter('Bad answer!', 255))
                    correct_answers.append(0)
                    sleep(2)
                    cleaner()
        else:
            print(line.rstrip())

    if all(correct_answers):
        print(painter(f'Congratulations {us_cl.nick} you finished quiz with every possible correct answer!, that gives us: {us_cl.quiz_points} points!', g=255, b=100))
    elif not any(correct_answers):
        print(painter(f'Sorry {us_cl.nick} you finished quiz without any correct answer...'))
    else:
        print(painter(f'Congratulations {us_cl.nick} you finished quiz with score {correct_answers.count(1)}/10, that gives us: {us_cl.quiz_points} points!'))
    sleep(4)


def painter(text: str, r:int = 0, g:int = 0, b:int = 0) -> str:
    return f'\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m'
