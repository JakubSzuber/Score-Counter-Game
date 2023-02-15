from time import sleep
import functions as func
import users


def main() -> None:
    leader_board: list[dict[str | int, int]] = []  # A list of each user who has finished all minigames

    while True:
        # Greeting the user and explain what it will do
        func.cleaner()
        func.start_window()

        with func.cm_sign_in_window(current_user := func.sign_in_window(leader_board)):  # Create instance of the class User and use context manager at one time
            current_user: users.User

        # Use the functions responsible for the mini-games one by one
        func.quiz(current_user)
        func.number_guessing(current_user)
        func.russian_schnapsen_game(current_user)
        func.memory_game(current_user)

        with func.CmEndWindow(r'C:\Users\jszub\PycharmProjects\Score-Counter-Game\logs.txt', 'a', current_user):
            print(current_user)  # Show to user earned points in each game and in the whole app

        leader_board.append({current_user.nick: current_user.all_points})  # Add user to the leader board

        # Showing leader board from best score to the worst one if the user whant to see it
        leader_board_show: str = input('If you want to see leader board enter "yes" and if you want to start new session enter anything else: ')

        if leader_board_show == 'yes':
            print('\n')
            leader_board.sort(key=lambda x: list(x.values())[0])

            for user in list(enumerate(leader_board, start=1)):
                if user[0] == 1:
                    print(func.painter(str(user), 212, 175, 55))
                elif user[0] == 2:
                    print(func.painter(str(user), 180, 180, 180))
                elif user[0] == 3:
                    print(func.painter(str(user), 173, 138, 86))
                else:
                    print(user)

            sleep(4.5)
        else:
            continue


if __name__ == '__main__':
    main()
