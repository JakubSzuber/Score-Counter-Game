import functions as funs

def main():
    leader_board = {}  # TODO: maybe the leader board should be done in the form of a class or function!

    funs.cleaner()
    user_chose = funs.start_window()
    funs.cleaner()
    current_user = funs.sing_in_window(user_chose)

    match user_chose:
        case 1:
            funs.quiz(current_user)
        case 2:
            funs.number_guessing(current_user)
        case 3:
            funs.russian_schnapsen_game(current_user)
        case 4:
            funs.memory_game(current_user)

    funs.saver(current_user, leader_board)
    #funs.end_window()


if __name__ == '__main__':
    main()
