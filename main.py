import functions as func

def main():
    leader_board = []

    while True:
        func.cleaner()
        func.start_window()  # Greeting the user and explain what will user do
        func.cleaner()

        current_user = func.sing_in_window()  # Create instance of the class User

        # Use the functions responsible for the mini-games one by one
        func.quiz(current_user)
        func.number_guessing(current_user)
        func.russian_schnapsen_game(current_user)
        func.memory_game(current_user)

        func.end_window_1(current_user)  # Show to user earned point in each game and in the whole app (use a few methods in class User)

        leader_board.append({current_user.nick: current_user.all_points})  # Add user to leader board

        leader_board_show = input('If you want to see leader board enter "yes" and if you want to start new session enter anything else: ')
        if leader_board_show == 'yes':
            leader_board.sort(key=lambda x: list(x.values())[0])
            for user in list(enumerate(leader_board, start=1)):
                print(user)
        else:
            continue


if __name__ == '__main__':
    main()
