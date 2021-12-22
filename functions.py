from time import sleep
import math

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


def sing_in_window():
    print('Before we start enter data:')
    user_nick = input('Your nick: ')
    print('Chose eventualy level of difficult:\n-normal\n-medium')
    diff_level = input('Your answer: ')
    curr_us = User(user_nick, diff_level)
    cleaner()
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
    print('We can start quiz now!')
    print('Choose what topic of the quiz you prefer: python or math?')
    quiz_topic = input('Your answer: ')
    cleaner()

    match user_class.level:

        case 'medium':
            print('You chose medium difficulty, you can get 150 points for the right answer!')
            if quiz_topic == 'python':
                print('Your answer shulod be correct to examplepattern: a\n')
                sleep(3)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_medium_quiz', 'r') as file:  # Here use absolute path of the file where you have file with content of teh quiz
                    quiz_body(user_class, file, 'python')
            else:
                print('Your answer shulod be correct to examplepattern: 2')
                sleep(3)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_medium_quiz', 'r') as file:
                    quiz_body(user_class, file, 'math')

        case 'normal':
            print('You chose normal difficulty, you can get 100 points for the right answer!')
            if quiz_topic == 'python':
                print('Your answer shulod be correct to examplepattern: a\n')
                sleep(3)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_normal_quiz', 'r') as file:
                    quiz_body(user_class, file, 'python')
            else:
                print('Your answer shulod be correct to examplepattern: 2')
                sleep(3)
                with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_normal_quiz', 'r') as file:
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
    cleaner()
    counter = 0
    for line in f:
        counter += 1

        if counter % 6 == 0:
            if quiz_type == 'math':
                correct_ans = eval(line.rstrip())
                user_answer = int(input('Your answer: '))
            else:
                correct_ans = line.rstrip()
                user_answer = input('Your answer: ')

            if user_answer == correct_ans:
                print('Good answer, you\'re getting points!')
                us_cl(150)  # Use mothod call in class User (add points to object)
                sleep(2)
                cleaner()
            else:
                print('Bad answer!')
                sleep(2)
                cleaner()
        else:
            print(line.rstrip())
