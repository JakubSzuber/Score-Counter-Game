import functions as func


def main():
    leader_board = []  # A list of each user who has finished all minigames

    while True:
        # Greeting the user and explain what it will do
        func.cleaner()
        func.start_window()

        with func.cm_sing_in_window(current_user := func.sing_in_window(leader_board)):  # Create instance of the class User and use context manager at one time
            pass

        # Use the functions responsible for the mini-games one by one
        func.quiz(current_user)
        func.number_guessing(current_user)
        func.russian_schnapsen_game(current_user)
        func.memory_game(current_user)

        with func.CmEndWindow(r'C:\Users\jszub\OneDrive\Pulpit\logs.txt', 'a', current_user):
            print(current_user)  # Show to user earned points in each game and in the whole app

        leader_board.append({current_user.nick: current_user.all_points})  # Add user to teh leader board

        # Showing leader board from best score to the worst one if the user whant to see it
        leader_board_show = input('If you want to see leader board enter "yes" and if you want to start new session enter anything else: ')
        if leader_board_show == 'yes':
            leader_board.sort(key=lambda x: list(x.values())[0])
            for user in list(enumerate(leader_board, start=1)):
                print(user)
        else:
            continue


if __name__ == '__main__':
    main()
