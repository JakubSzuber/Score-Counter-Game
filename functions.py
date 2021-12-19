# Different windows:
def start_window():
    print('Hello user!')
    print('You can choose one of several options, where to start completing tasks and collecting points. Good luck!')
    print('Choose one option:')
    print('Enter 1 - to start quiz.')  # TODO
    print('Enter 2 - to start game.')  # TODO
    print('Enter 3 - to start applocations.')  # TODO
    print('Enter 0 to open pause menu.')
    print('-'*20)
    user_selection = int(input('Your answer: '))
    return user_selection


def sing_in_window():
    print('Before we start enter data:')
    user_nick = input('Your nick: ')
    print('Chose level of difficult:\n-easy\n-hard')
    diff_level = int(input('Your answer: '))
    return user_nick, diff_level  # TODO may return these variables in a different way?


def end_window():  # TODO to finish writing this window you need a finite User class !!!
    pass


def pause_menu_window():
    print(10*'-', 'Pause menu', 10*'-',)
    print('Enter 1 to xxx...')
    print('Enter 2 to xxx...')
    print('Enter 3 to xxx...')
    print('-'*20)



# Sub-applications:
def exec_quiz():
    print('We starting quiz!')
    pass  # TODO whole body of the quiz


def ball_game():
    print('We starting ball game!')
    pass  # TODO whole body of the ball game


def applications():
    print('We\'re starting page of the applications')
    pass  # TODO whole body of the applications



# Auxiliary functions and temporary functions:
def cleaner():  # TODO think is it a good idea
    print(20*'\n')


def saver(nick, level, board):
    board.append(nick+': '+level)
