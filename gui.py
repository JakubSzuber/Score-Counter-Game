# File for testing an app with GUI

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
from time import sleep
import functions as func
import users
import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image
import sys


customtkinter.set_appearance_mode("System")  # XXX
customtkinter.set_default_color_theme("blue")  # XXX

pause_img = customtkinter.CTkImage(Image.open('pause.webp'))
see_logs_img = customtkinter.CTkImage(Image.open('see_logs.png'))
export_logs_img = customtkinter.CTkImage(Image.open('export_logs.png'), size=(18, 18))

# A global variable which counts the user's correct answers
correct_answers: list[int] = []

# A global list of each user who has finished all minigames
leader_board: list[dict[str | int, int]] = []

# Other global variables



global quiz_topic
quiz_topic: str

global choosen_range
choosen_range: int

global current_user
current_user: users.User

# XXX
class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Score-Counter-Game")
        self.geometry(f"{1100}x{580}")
        self.minsize(900, 460)

        # Configure grid layout (6x3)
        self.grid_columnconfigure((1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # Sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="ns")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text=" Leader Board", font=customtkinter.CTkFont(size=28, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, corner_radius=15, border_width=2)  # TODO make it sticky to ns
        self.textbox.grid(row=1, column=0, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.switch_var = customtkinter.StringVar(value="on")
        self.appearance_mode_optionemenu = customtkinter.CTkSwitch(self.sidebar_frame, variable=self.switch_var, onvalue="on", offvalue="off", command=self.change_appearance_mode_event, text="Dark")
        self.appearance_mode_optionemenu.grid(row=3, column=0, padx=20, pady=(5, 15))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=5, column=0, padx=20, pady=(5, 25))


        # Output frame
        self.textbox = customtkinter.CTkTextbox(self, width=140, corner_radius=20, font=customtkinter.CTkFont(size=40))
        self.textbox.grid(row=0, column=1, columnspan=4, rowspan=2, sticky="nsew", padx=20, pady=(15, 0))
        self.textbox.insert("0.0", 'If your\'re ready click Submit')
        self.textbox.configure(state="disabled")

        # self.output_frame = customtkinter.CTkFrame(self, width=140, corner_radius=20)
        # self.output_frame.grid(row=0, column=1, columnspan=4, rowspan=2, sticky="nsew", padx=20, pady=(15, 0))
        #
        # self.output_label = customtkinter.CTkLabel(master=self.output_frame, text="\nIf you are ready click Submit", font=customtkinter.CTkFont(size=28, weight="bold"))
        # self.output_label.pack(padx=10, pady=10)


        # User input and submit button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Input anwser", font=customtkinter.CTkFont(size=23))  # TODO center cursor
        self.entry.grid(row=2, column=1, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Submit", hover_color="#20bf7e", font=customtkinter.CTkFont(size=17), command=user_submit)
        self.main_button_1.grid(row=2, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # Options frame
        self.options_frame = customtkinter.CTkFrame(self, corner_radius=15)
        self.options_frame.grid(row=0, column=5, rowspan=3, padx=(0, 20), pady=(20, 20), sticky="ns")

        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.options_frame, text="Event Buttons", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")

        self.pause_button = customtkinter.CTkButton(master=self.options_frame, text="Pause Game", command=self.pause, image=pause_img)
        self.pause_button.grid(row=1, column=2, pady=10, padx=20, sticky="n")

        self.see_logs_button = customtkinter.CTkButton(master=self.options_frame, text="See logs", command=self.see_logs, image=see_logs_img)
        self.see_logs_button.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        self.export_button = customtkinter.CTkButton(master=self.options_frame, text="Export logs", command=self.export_logs, image=export_logs_img)
        self.export_button.grid(row=3, column=2, pady=10, padx=20, sticky="n")


        # Set default values
        self.textbox.configure(state="disabled")
        self.scaling_optionemenu.set("100%")
        self.appearance_mode_optionemenu.select()


    def change_appearance_mode_event(self):  # TODO fix problem with not changing .text
        if self.switch_var.get() == "on":
            customtkinter.set_appearance_mode("Dark")
            self.appearance_mode_optionemenu.text="Dark"
        else:
            customtkinter.set_appearance_mode("Light")
            self.appearance_mode_optionemenu.text="Light"


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def pause(self):
        pass

    def see_logs(self):
        pass

    def export_logs(self):
        pass

# XXX
class StartWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Score-Counter-Game")
        self.geometry(f"{600}x{350}")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        background_img = customtkinter.CTkImage(Image.open("background.jpg"), size=(950, 350))
        self.img_base = customtkinter.CTkLabel(master=self, image=background_img)
        self.img_base.grid(row=0, column=0, sticky="nsew")

        self.frame = customtkinter.CTkFrame(master=self.img_base, width=320, height=360, corner_radius=15)
        self.frame.grid(row=0, column=0, columnspan=3, rowspan=3, padx=20, pady=25, sticky="nsew")

        self.frame.columnconfigure((0, 2), weight=1)

        self.welcome_text_1 = customtkinter.CTkLabel(master=self.frame, text="Score-Counter-Game", font=customtkinter.CTkFont(size=35, weight="bold"))
        self.welcome_text_1.grid(row=1, column=1, pady=(30, 5))

        self.welcome_text_2 = customtkinter.CTkLabel(master=self.frame, text="Made by: Jakub Szuber", font=customtkinter.CTkFont(size=15))
        self.welcome_text_2.grid(row=2, column=1)

        self.start_button = customtkinter.CTkButton(master=self.frame, command=main_opener, width=300, height=55, corner_radius=10, fg_color="green", border_color="#064503", border_width=1, hover_color="#12780e", text="Start the game")
        self.start_button.grid(row=3, column=1, pady=(50, 0))



    # leader_board: list[dict[str, int]] = []  # A list of each user who has finished all minigames
    #
    # while True:
    #     # Greeting the user and explain what it will do
    #     func.cleaner()
    #     # func.start_window()
    #
    #     with func.cm_sign_in_window(current_user := func.sign_in_window(
    #             leader_board)):  # Create instance of the class User and use context manager at one time
    #         current_user: users.User
    #
    #     # Use the functions responsible for the mini-games one by one
    #     # func.quiz(current_user)
    #     # func.number_guessing(current_user)
    #     # func.russian_schnapsen_game(current_user)
    #     # func.memory_game(current_user)
    #
    #     with func.CmEndWindow(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\logs.txt', 'a', current_user):
    #         print(current_user)  # Show to user earned points in each game and in the whole app
    #
    #     leader_board.append({current_user.nick: current_user.all_points})  # Add user to the leader board
    #
    #     # Showing leader board from best score to the worst one if the user whant to see it
    #     leader_board_show: str = input(
    #         'If you want to see leader board enter "yes" and if you want to start new session enter anything else: ')
    #
    #     if leader_board_show == 'yes':
    #         print('\n')
    #         leader_board.sort(key=lambda x: list(x.values())[0])
    #
    #         for user in list(enumerate(leader_board, start=1)):
    #             if user[0] == 1:
    #                 print(func.painter(user, 212, 175, 55))
    #             elif user[0] == 2:
    #                 print(func.painter(user, 180, 180, 180))
    #             elif user[0] == 3:
    #                 print(func.painter(user, 173, 138, 86))
    #             else:
    #                 print(user)
    #
    #         sleep(4.5)
    #     else:
    #         continue

def main_opener():
    global counter
    counter = 0

    app.destroy()
    global main_win
    main_win = MainWindow()
    main_win.mainloop()


# --------------------- Context managers and wrappers ---------------------
@contextmanager
def cm_sign_in_window(user: User) -> None:
    yield
    with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\logs.txt', 'a') as file:  # Used absolute path of the file in which are stored logs from app
        file.write(f'\n{user.nick} started playing at {datetime.now()}\n')
    add_output('Saving succesful!', 25, "4.0")

class CmEndWindow:
    def __init__(self, path: str, method: str, current_user: User) -> None:
        self.file_obj: TextIO = open(path, method)
        self.current_user: User = current_user

    def __enter__(self) -> None:
        correct_answers.clear()
        add_output('This is end of the application!', 25, "1.0")
        add_output('\n\n', 25, "2.0")
        add_output('Saving overall score into file, pleas wait...\n', 25, "3.0")
        self.file_obj.write(f'{self.current_user.nick} end with score: {self.current_user.all_points}\n')
        add_output('Saving succesful!', 25, "4.0")
        sleep(4)

    def __exit__(self, exc_type: str, exc_val: str, exc_tb: str) -> None:
        self.file_obj.close()

class CmGreenText:
    def __enter__(self) -> None:
        main_win.textbox.configure(text_color="green")

    def __exit__(self, exc_type: str, exc_val: str, exc_tb: str) -> None:
        main_win.textbox.configure(text_color="white")


class CmRedText:
    def __enter__(self) -> None:
        main_win.textbox.configure(text_color="red")

    def __exit__(self, exc_type: str, exc_val: str, exc_tb: str) -> None:
        main_win.textbox.configure(text_color="white")

def error_handler(function: Callable):
    def arguments(*args):
        while True:
            try:
                on = function(*args)
            except ValueError as e:
                main_win.textbox.configure(text_color="red")
                clean_output()
                add_output('You entered wrong type of the value!', 25, "1.0")
                error_hendler_content(e)
            except AssertionError as e:
                main_win.textbox.configure(text_color="red")
                clean_output()
                add_output('A logic of the program has broken!\n', 25, "1.0")
                error_hendler_content(e)
            except (FileNotFoundError, FileExistsError) as e:
                main_win.textbox.configure(text_color="red")
                clean_output()
                add_output('Appeared error with file path!', 25, "1.0")
                error_hendler_content(e)
            except Exception as e:
                main_win.textbox.configure(text_color="red")
                clean_output()
                add_output('Appeared unexpected error!', 25, "1.0")
                error_hendler_content(e)
            else:
                break
        return on
    return arguments

def error_hendler_content(e):
    add_output(f'Details:', 25, "2.0")
    add_output('\n\n', 25, "3.0")
    add_output(str(e), 25, "4.0")

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


# --------------------- General functions ---------------------
def welcome(queue_num: int) -> None:
    if queue_num == 0:
        add_output('Hello user!', 25, "1.0")
        add_output('\n\n', 25, "2.0")
        add_output('You will be playing in few games, where you can completing tasks and collecting points. When you end all four minigames you could see leader board and start playing anew. Good luck!', 25, "3.0")
        add_output('\n\n', 25, "4.0")
        add_output('Follow the guidelines carefully because if you cause an error you probably will have to play mini-game from the begining!', 25, "5.0")
        add_output('\n\n', 25, "6.0")
        add_output('Click submit button to see list of games', 25, "7.0")
    else:
        clean_output()
        add_output('Here is the list of games that you will play sequentially:\n', 25, "1.0")
        add_output('1 - quizzes about math or python\n', 25, "2.0")
        add_output('2 - number guessing game\n', 25, "3.0")
        add_output('3 - russian schnapsen game (card game)\n', 25, "4.0")
        add_output('4 - color-number memory game\n', 25, "5.0")
        add_output('-'*72, 25, "6.0")
        add_output('\n\n', 25, "7.0")
        add_output('Click submit button to finally start the game!', 25, "8.0")

@error_handler
def sign_in_window(l_board: list[dict[str, int]], queue_num: int) -> User:
    match queue_num:
        case 2:
            add_output('Before we start enter data:', 25, "1.0")
            add_output('\n\n', 25, "2.0")
            add_output('Your nick:', 25, "3.0")
        case 3:
            global user_nick

            user_nick = main_win.entry.get()

            main_win.entry.delete(0, "end")

            assert user_nick not in l_board, 'User with this nick is already saved in the leader board!'
            assert user_nick != '', 'Your nick must have characters!'

            add_output('Choose level of difficult in quiz:\n', 25, "1.0")
            add_output('-normal\n', 25, "2.0")
            add_output('-medium', 25, "3.0")
        case 4:
            diff_level: str = main_win.entry.get()

            main_win.entry.delete(0, "end")

            assert diff_level == ('normal' or 'medium'), 'You entered wrong level of the difficulty (typo)!'

            curr_us: User = User(user_nick, diff_level)
            return curr_us


# --------------------- Minigames applications ---------------------
@error_handler
@minigame_wrapper('quiz')
def quiz(user_class: User, queue_num: int) -> None:
    match queue_num:
        case 2:
            add_output('-------We can start quiz now!-------\n', 25, "1.0")
            add_output('Choose what topic of the quiz you prefer: python or math?', 25, "2.0")
        case 3:
            quiz_topic: str = main_win.entry.get()
            assert quiz_topic == 'python' or 'math', 'You entered wrong type of the quiz (typo)!'

            match user_class.level:
                case 'medium':
                    add_output('You chose medium difficulty, you can get 150 points for the right answer!\n', 25, "1.0")
                    if quiz_topic == 'python':
                        add_output('Your answer should be correct to example pattern: a\n', 25, "2.0")
                        sleep(5)
                        with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_medium_quiz', 'r') as file:  # Used absolute path of the file where is content of the quiz
                            quiz_body(user_class, file, 'python')
                    else:
                        add_output('Your answer should be correct to example pattern: 2\n', 25, "2.0")
                        sleep(5)
                        with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_medium_quiz', 'r') as file:
                            quiz_body(user_class, file, 'math')
                case 'normal':
                    add_output('You chose normal difficulty, you can get 100 points for the right answer!', 25, "1.0")
                    if quiz_topic == 'python':
                        add_output('Your answer should be correct to example pattern: a\n', 25, "2.0")
                        sleep(5)
                        with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\python_normal_quiz', 'r') as file:
                            quiz_body(user_class, file, 'python')
                    else:
                        add_output('Your answer should be correct to example pattern: 2\n', 25, "2.0")
                        sleep(5)
                        with open(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\data\math_normal_quiz', 'r') as file:
                            quiz_body(user_class, file, 'math')


@error_handler
@lru_cache
def quiz_body(us_cl: User, f: TextIO, quiz_type: str) -> None:  # Argument "f" is a file reference
    line_counter: int = 0

    for line in f:
        line_counter += 1

        if line_counter % 6 == 0:
            user_answer: str = input('Your answer: ')
            add_output('\n\n', 25, "3.0")
            add_output('Your answer:', 25, "4.0")

            assert user_answer != '', 'You didn\'t select any answer!'


            if quiz_type == 'math':
                correct_ans = eval(line.rstrip())
                if float(user_answer) == correct_ans:
                    with CmGreenText:
                        add_output('Good answer, you\'re getting points!', 25, "1.0")
                        us_cl += 150  # Use method __iadd__() in class User (add points to object)
                        us_cl.quiz_points += 150
                        correct_answers.append(1)
                        sleep(2)
                else:
                    with CmRedText:
                        add_output('Bad answer!', 25, "1.0")
                        correct_answers.append(0)
                    sleep(2)
            else:
                correct_ans = line.rstrip()
                if user_answer == correct_ans:
                    with CmGreenText:
                        add_output('Good answer, you\'re getting points!', 25, "1.0")
                        us_cl += 150
                        us_cl.quiz_points += 150
                        correct_answers.append(1)
                    sleep(2)
                else:
                    with CmRedText:
                        add_output('Bad answer!', 25, "1.0")
                        correct_answers.append(0)
                    sleep(2)
        else:
            add_output(line.rstrip(), 25, "1.0")

    if all(correct_answers):
        with CmGreenText:
            add_output(f'Congratulations {us_cl.nick} you finished quiz with every possible correct answer!, that gives us: {us_cl.quiz_points} points!', 25, "1.0")
    elif not any(correct_answers):
        with CmRedText:
            add_output(f'Sorry {us_cl.nick} you finished quiz without any correct answer...', 25, "1.0")
    else:
        with CmGreenText:
            add_output(f'Congratulations {us_cl.nick} you finished quiz with score {correct_answers.count(1)}/10, that gives us: {us_cl.quiz_points} points!', 25, "1.0")
    sleep(4)


@error_handler
@minigame_wrapper('number guessing')
def number_guessing(user_class: User, queue_num: int) -> None:  # TODO logic of that function have to be enhanced later
    match queue_num:
        case 8:
            add_output('-------We can start number guessing game now!-------\n', 25, "1.0")
            add_output('Below rules of the game:\n', 25, "2.0")
            add_output('-You will choose range of the number to quess one number from this range\n', 25, "3.0")
            add_output('-The lowest possible number is 0\n', 25, "4.0")
            add_output('-You have no limit of trials untill you quess the number\n', 25, "5.0")
            add_output('-Program will help you to guess it\n', 25, "6.0")
            add_output('-Remember the larger the range you choose and the faster you guess the number, the more points you get!\n', 25, "7.0")
            add_output('-Your answer should be correct to example pattern: 35\n', 25, "8.0")
            add_output('\n\n', 25, "9.0")

            add_output('If you read rules you can choose the range of the possible numbers (e.g. 100):', 25, "10.0")
            choosen_range: int = main_win.entry.get()
            assert choosen_range >= 2, 'You chosen to small range of the numbers'
        case 9:
            add_output('Finally we can start game!', 25, "1.0")
            sleep(2)
        case 10:
            drawn_num: int = randint(0, choosen_range)
            guess_counter: int = 0

            add_output('Guess number: ', 25, "1.0")
            user_trial: int = main_win.entry.get()
            guess_counter += 1

            while user_trial != drawn_num:
                if user_trial < drawn_num:
                    add_output('Too small number!\n', 25, "1.0")
                    user_trial: int = main_win.entry.get()
                    add_output('Guess number: ', 25, "1.0")
                    guess_counter += 1
                elif user_trial > drawn_num:
                    add_output('Too big number!\n', 25, "1.0")
                    user_trial: int = main_win.entry.get()
                    add_output('Guess number: ', 25, "1.0")
                    guess_counter += 1
            else:
                with CmGreenText:
                    earned_points: int = choosen_range//guess_counter*10
                    user_class += earned_points
                    user_class.num_guess_points += earned_points
                    add_output(f'Congratulations {user_class.nick}, you quess correct after {guess_counter} times!', 25, "1.0")
                    add_output(f'You earned {earned_points} points', 25, "2.0")
                sleep(3.5)



# --------------------- Other functions ---------------------
def add_output(new_text: str, new_size: int, line: str):
    print('Function started..')

    main_win.textbox.configure(state="normal")

    current_text = main_win.textbox.get("0.0", "end")
    print(f'Current text: {current_text}')
    main_win.textbox.insert(line, new_text)
    main_win.textbox.configure(font=customtkinter.CTkFont(size=new_size, weight="bold"))
    #main_win.textbox.insert(text=current_text+new_text, font=customtkinter.CTkFont(size=new_size, weight="bold"))
    print(f'Current text: {new_text}')

    main_win.textbox.configure(state="disabled")


def clean_output():
    main_win.textbox.configure(state="normal")
    main_win.textbox.delete("0.0", "end")
    main_win.textbox.configure(state="disabled")


def user_submit():

    global counter
    match counter:
        case 0 | 1:
            clean_output()
            welcome(counter)
        case 2 | 3:
            clean_output()
            sign_in_window(leader_board, counter)
        case 4:
            clean_output()
            add_output('Your nick and time of staring playing will be saved into file (and your every activity in this game)', 25, "1.0")
            add_output('\n\n', 25, "2.0")
            add_output('Saving, pleas wait...\n', 25, "3.0")
            sleep(3)
            with cm_sign_in_window(current_user := sign_in_window(leader_board, counter)):  # Create instance of the class User and use context manager at one time
                pass
        case _:
            print('nie')

    counter+=1


# def test3():
#
#     input_value = main_win.entry.get()
#     print(input_value)
#
#     if input_value == "yes":
#         clean_output()
#         add_output('You are!', 25, "0.0")
#     else:
#         clean_output()
#         add_output('That\'s not good!', 25, "0.0")
#     main_win.entry.delete(0, "end")


if __name__ == '__main__':
    global app
    app = StartWindow()
    app.mainloop()
