import functions as funs

def main():
    leader_board = []  # TODO here will be successively saved users with their result and place in the table
    # TODO !: maybe the leader board should be done in the form of a class, not a list!

    funs.cleaner()
    funs.start_window()
    funs.cleaner()
    funs.sing_in_window()
    match funs.start_window():
        case 1:
            funs.exec_quiz()
        case 2:
            funs.ball_game()
        case 3:
            funs.applications()


if __name__ == '__main__':
    main()
