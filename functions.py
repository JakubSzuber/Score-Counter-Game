import itertools
from time import sleep
import math
import random
import string

from users import User


# Different windows:
def start_window():
    print('Hello user!')
    print('You can choose one of several options, where to start completing tasks and collecting points. Good luck!')
    sleep(4)
    cleaner()
    print('Choose one option:')
    print('Enter 1 - to start one of the quizzes.')
    print('Enter 2 - to start number guessing game.')
    print('Enter 3 - to start card game.')
    print('Enter 4 - to start memory game.')
    #print('Enter 0 to open pause menu.')
    print('-'*20)
    user_selection = int(input('\tYour answer: '))
    return user_selection


def sing_in_window(user_sel):
    print('Before we start enter data:')
    user_nick = input('Your nick: ')
    if user_sel == 1:
        print('\nChose eventualy level of difficult:\n-normal\n-medium')
        diff_level = input('Your answer: ')
        curr_us = User(user_nick, diff_level)
    else:
        curr_us = User(user_nick)
    cleaner()
    return curr_us


def end_window(user_class):
    print(painter('Congratulations {user_class.nick}!', g=255, b=100))
    print(painter(f'You overall scored: {user_class.points}', g=255, b=100))


def pause_menu_window():  # TODO to create this window is required npyscreen (a Python curses wrapper)
    print(10*'-', 'Pause menu', 10*'-')
    print(painter('Enter 1 to see how much time have you playing', 192, 192, 192))
    print(painter('Enter 2 to see how much points have you scored', 192, 192, 192))
    print(painter('Enter 3 to end game', 192, 192, 192))
    print(painter('-'*20, 192, 192, 192))



# Sub-applications:
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

    drawn_num = random.randint(0, choosen_range)
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
        print(painter(f'Gangratulations {user_class.nick}, you quess correct after {counter} times!', g=255))
        print(painter(f'You earned {earned_points} points', g=255))


def card_game(user_class):
    print('We\'re starting card game')
    pass  # TODO whole body of the applications


def memory_game(user_class):
    print(painter('We can start memory game now!', g=255, b=100))
    print(painter('Below rules of the first part of game:', 255))
    print(painter('-XXX..', 200))  # tODO
    print(painter('-XXX..', 200))
    print(painter('-XXX..', 200))
    print(painter('-XXX..', 200))

    input('If you\'re ready enter anything: ')
    print('Finally we can start game!')
    sleep(2)
    cleaner()

    iterator = 100
    while True:
        print('Number:', secret_num := random.randint(iterator, iterator*2))
        sleep(3)
        cleaner()

        users_trial = int(input('Enter number: '))

        if users_trial == secret_num:
            print(painter(f'Correct answer! You get {iterator//20} points!', g=255))
            user_class += iterator//20
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
    print(painter('-XXX..', 200))  # tODO
    print(painter('-XXX..', 200))
    print(painter('-XXX..', 200))
    print(painter('-XXX..', 200))

    input('If you\'re ready enter anything: ')
    print('Finally we can start game!')
    sleep(2)
    cleaner()

    colors = ['red', 'green', 'blue', 'pink']
    chars_num = list(itertools.chain(string.digits, string.ascii_letters))
    counter = 2

    while True:
        if counter == 60:
            print('Incredible score! You\'ve got maximum points form part two!')
            break

        gen_password = random.sample(chars_num, counter)
        gen_color = random.choice(colors)

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
            user_class += 100
        else:
            print(painter('Sorry bad answer! Second part of game is over!', 255))
            break

        user_color_answer = input('Enter the color of teh password: ')
        if gen_color == user_color_answer:
            print(painter('Correct answer you\'re getting points!', g=255))
            sleep(2)
            user_class += 50
        else:
            print(painter('Sorry bad answer! Second part of game is over!', 255))
            break

        cleaner()

        counter += 1



# Auxiliary functions and temporary functions:
def cleaner():  # TODO change this function in npyscreen (a Python curses wrapper) in the future
    print(20*'\n')


def saver(user_class, board):
    board[user_class.nick] = user_class.points


def quiz_body(us_cl, f, quiz_type):
    cleaner()
    counter = 0
    for line in f:
        counter += 1

        if counter % 6 == 0:
            user_answer = input('Your answer: ')
            if quiz_type == 'math':
                correct_ans = eval(line.rstrip())
                if float(user_answer) == correct_ans:
                    print('Good answer, you\'re getting points!')
                    us_cl += 150  # Use mothod call in class User (add points to object)
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
                    sleep(2)
                    cleaner()
                else:
                    print('Bad answer!')
                    sleep(2)
                    cleaner()
        else:
            print(line.rstrip())

    print(f'Congratulations {us_cl.nick} you finished quiz with score: {us_cl.poins}')  # TODO expand end of the quizz


def painter(text, r=0, g=0, b=0):
    return f'\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m'
