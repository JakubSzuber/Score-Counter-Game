# File for testing an app with GUI

from time import sleep
import functions as func
import users
import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image

customtkinter.set_appearance_mode("System")  # XXX
customtkinter.set_default_color_theme("blue")  # XXX


# XXX
def main_opener():
    app.destroy()
    main_win = MainWindow()
    main_win.mainloop()


# XXX
class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Score-Counter-Game")
        self.geometry(f"{1250}x{600}")
        self.minsize(800, 500)

        self.welcome_text_1 = customtkinter.CTkLabel(master=self, text="Score-Counter-Game", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.welcome_text_1.grid(row=0, column=3, pady=(20, 0))

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


if __name__ == "__main__":
    app = StartWindow()
    app.mainloop()
