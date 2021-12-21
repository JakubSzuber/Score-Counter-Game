from time import sleep
import math

from users import User


# Different windows:
def start_window():
    print('Hello user!')
    print('You can choose one of several options, where to start completing tasks and collecting points. Good luck!')
    print('Choose one option:')
    print('Enter 1 - to start one of the quizzes.')
    print('Enter 2 - to start number guessing.')
    print('Enter 3 - to start card game.')
    print('Enter 4 - to start memory game.\n')
    #print('Enter 0 to open pause menu.')
    print('-'*20)
    user_selection = int(input('\tYour answer: '))
    return user_selection


def sing_in_window():
    print('Before we start enter data:')
    user_nick = input('Your nick: ')
    print('Chose eventualy level of difficult:\n-easy\n-hard')
    diff_level = input('Your answer: ')
    curr_us = User(user_nick, diff_level)
    return curr_us


def end_window(user_class):
    print(f'Congratulations {user_class.nick}!')
    print(f'You scored: {user_class.points}')


def pause_menu_window():  # TODO to create this window is required npyscreen (a Python curses wrapper)
    print(10*'-', 'Pause menu', 10*'-')
    print('Enter 1 to see how much time have you playing')
    print('Enter 2 to see how much points have you scored')
    print('Enter 3 to end game')
    print('-'*20)



# Sub-applications:
def quiz(user_class):
    print('We starting quiz!')
    print('Choose what topic of the quiz you prefer: python or math?')
    quiz_topic = input('Your answer: ')

    match user_class.level:

        case 'hard':
            print('You chose hard difficulty, you can get 150 points for the right answer!')
            if quiz_topic == 'python':
                print('Your answer shulod be correct to examplepattern: a')
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_hard_quiz', 'r') as file:  # Here use absolute path of the file where you have file with content of teh quiz
                    quiz_body(user_class, file, 'python')
            else:
                print('Your answer shulod be correct to examplepattern: 2')
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_hard_quiz', 'r') as file:
                    quiz_body(user_class, file, 'math')

        case 'easy':
            print('You chose easy difficulty, you can get 100 points for the right answer!')
            if quiz_topic == 'python':
                print('Your answer shulod be correct to examplepattern: a')
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_easy_quiz', 'r') as file:
                    quiz_body(user_class, file, 'python')
            else:
                print('Your answer shulod be correct to examplepattern: 2')
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_easy_quiz', 'r') as file:
                    quiz_body(user_class, file, 'math')


def number_guessing():
    print('We starting number guessing game!')
    pass  # TODO whole body of the applications


def card_game():
    print('We\'re starting card game')
    pass  # TODO whole body of the applications


def memory_game():
    print('We\'re starting memory game!')
    pass  # TODO whole body of the applications



# Auxiliary functions and temporary functions:
def cleaner():  # TODO change this function in npyscreen (a Python curses wrapper) in the future
    print(20*'\n')


def saver(user_class, board):
    board[user_class.nick] = user_class.points


def quiz_body(us_cl, f, quiz_type):
    counter = 0
    for line in f:
        counter += 1

        if counter % 6 == 0:
            if quiz_type == 'math':
                correct_ans = eval(line.rstrip())
            else:
                correct_ans = line.rstrip()

            user_answer = int(input('Your answer: '))
            if user_answer == correct_ans:
                print('Good answer, you\'re getting points!')
                us_cl(150)  # Use mothod call in class User (add points to object)
                sleep(2)
            else:
                print('Bad answer!')
        else:
            print(line.rstrip())
