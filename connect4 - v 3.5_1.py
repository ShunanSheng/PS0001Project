import numpy as np
from random import randint
import time


class Game:
    def __init__(self, rows=6, cols=7, turn=1, wins=4):
        self.rows = rows
        self.cols = cols
        self.turn = turn
        self.wins = wins
        self.mat = None

    def create_board(self):
        return np.zeros((self.rows, self.cols))


def check_move(game, chosen_col, pop):  # needs inspectation
    if pop:
        if game.mat[0][chosen_col] == game.turn:
            return True
        else:
            return False
    else:
        if game.mat[game.rows - 1][chosen_col] == 0:
            return True
        else:
            return False


def update_game_turn(game):
    game.turn += 1
    if game.turn % 2 == 0:
        game.turn = 2
    else:
        game.turn = 1
    return game.turn


def apply_move(game, chosen_col, pop):
    if pop:  # 1 for pop out;0 for add on
        for i in range(0, game.rows - 1):
            game.mat[i][chosen_col] = game.mat[i + 1][chosen_col]
        game.mat[game.rows - 1][chosen_col] = 0
    else:
        i = 0
        while game.mat[i][chosen_col] != 0:
            i += 1
        row = i
        # print(i)
        game.mat[row][chosen_col] = game.turn
    update_game_turn(game)
    return game


def check_victory(game):  # how to define draw or pass on

    # check horizontal condition
    for player in range(1, 3):
        # print(piece)
        for i in range(game.rows):
            signal = 0  # check rows
            for j in range(game.cols):
                if game.mat[i][j] == player:
                    signal += 1
                    # print(signal)
                    if signal >= game.wins:
                        return player
                else:
                    signal = 0

        # print("row check done")
        # check vertical condition
        for j in range(0, game.cols):
            signal = 0
            for i in range(0, game.rows):
                if game.mat[i][j] == player:
                    signal += 1
                    # print(signal)
                    if signal >= game.wins:
                        return player
                else:
                    signal = 0
        # print("col check done")

        # check nagative sloped diagonals
        for i in range(0, game.rows - game.wins + 1):  # check rows
            for j in range(0, game.cols - game.wins + 1):
                signal = 0
                for k in range(0, game.wins):
                    if game.mat[i + k][j + k] == player:
                        signal += 1
                        # print(signal)
                        if signal >= game.wins:
                            return player
                    else:
                        signal = 0
        # print("- diagonal check done")
        # check positive sloped digonals
        for i in range(game.rows - game.wins + 1):  # check rows
            for j in range(game.wins - 1, game.cols):
                signal = 0
                for k in range(0, game.wins):
                    if game.mat[i + k][j - k] == player:
                        signal += 1
                        # print(signal)
                        if signal >= game.wins:
                            return player
                    else:
                        signal = 0
        # print("+ diagonal check done")

    for i in range(game.rows):
        for j in range(game.cols):
            if game.mat[i][j] == 0:
                return 0
    return 3


def display_board(game):
    for i in range(game.rows - 1, -1, -1):
        for j in range(game.cols):
            print(int(game.mat[i][j]), end=' ')
        print()


def choose_col(game):  # Changed by ZSZ
    print('Player ', game.turn, "please choose a column to drop the piece (from 1 to ", game.cols, '):\n')
    chosen_col = input()
    while not (chosen_col.isdigit() == True and int(chosen_col) <= game.cols):
        print('Your input value is invalid! Please enter again')
        chosen_col = input()
    else:
        chosen_col = int(chosen_col) - 1
    return chosen_col


# Modified Oct 29


def choose_add_on_method(game):
    print('Please choose the way to add the piece (1 for pop out, 0 for add on):\n')
    pop = input()
    while (not pop.isdigit()) or not (int(pop) == 1 or int(pop) == 0):
        print("Invalid move!")
        pop = input()
    # Checking whether the input value is valid, if not, prompt the user for input again until a valid value is obtained
    return int(pop)


def human_move(game):
    col = choose_col(game)
    pop = choose_add_on_method(game)

    while True:
        if check_move(game, col, pop):
            game = apply_move(game, col, pop)
            break
        else:
            print("Invalid input!")
            col = choose_col(game)
            pop = choose_add_on_method(game)


def check_and_print_winner(game):
    victory_condition = check_victory(game)
    if victory_condition == 0:
        pass
    elif victory_condition == 1:
        print("Congrats!Player 1 wins!")
    elif victory_condition == 2:
        print("Congrats!Player 2 wins!")
    else:
        print("Ooh,it is a draw!")
    return victory_condition


def add_mode():
    mode = input('PvP or PvC?: Please enter 1 for PvP mode, 2 for PvC mode')
    if mode == '1':
        mode = 0
    elif mode == '2':
        print('Which difficulty level do you choose?(easy:1,medium:2,difficult:3):')
        mode = int(input())
        if mode < 1 or mode > 3:
            print('Invalid input!')
            mode = int(input('Enter the diffculty level!(easy:1,medium:2,difficult:3)'))
    else:
        print("Invalid input!")
        mode = input('PvP or PvC?:Please enter 1 for PvP mode, 2 for PvC mode')
    return mode


# Modified Oct 29
# Ask user to choose game mode. In consideration of the convenience of users and in order to improve input-checking process ,
# only digits are asked to be keyed in, instead of a string.
# Use will be prompted to key in the valid values if input error occurs.

def menu():
    game = Game()
    game.rows = input("How many rows?")
    while not (game.rows.isdigit() == True and int(game.rows) >= 3):
        # In addition to obtaining integers, this checking also requires a value not less than 3 to ensure the game is normally played.
        print('Your input value is invalid! Please enter again')
        # Use will be prompted to key in the valid values if input error occurs.
        game.rows = input()
    else:
        game.rows = int(game.rows)
    game.cols = input("How many columns?:")
    while not (game.cols.isdigit() == True and int(game.cols) >= 3):
        print('Your input value is invalid! Please enter again')
        game.cols = input()
        # Use will be prompted to key in the valid values if input error occurs.
    else:
        game.cols = int(game.cols)
    game.wins = input("How many wins:")
    while not (game.wins.isdigit() == True and int(game.wins) <= game.rows):
        print('Your input value is invalid! Please enter again')
        # Use will be prompted to key in the valid values if input error occurs.
        game.wins = input()
    else:
        game.wins = int(game.wins)

    # Modified Oct 29
    game.turn = randint(1, 2)
    # The turns of the game is randomly decided.
    game.mat = np.zeros((game.rows, game.cols))
    mode = add_mode()
    game_over = False

    while not game_over:
        if game.turn == 1:
            if mode == 0:
                human_move(game)
                display_board(game)
            if mode != 0:
                try_to_think()
                (col, pop) = computer_move(game, mode)
                game = apply_move(game, col, pop)
                display_board(game)
            condition = check_and_print_winner(game)
            if condition != 0:
                game_over = True
        else:
            human_move(game)
            display_board(game)
            condition = check_and_print_winner(game)
            if condition != 0:
                game_over = True


def try_to_think():
    print("CPU will make the move!")
    print("CPU is thinking...")
    time.sleep(3)
    # In consideration of the gaming experience, we added this feature to the game, which is, to simulate the thinking process
    # of computer.

    # PVC: east-level


def computer_level_easy(game):
    # computer randomly choose the (col,pop)
    cpu_level_easy_col = randint(0, game.cols - 1)
    cpu_level_easy_pop = randint(0, 1)
    # check validity of the move generated
    while not check_move(game, cpu_level_easy_col, cpu_level_easy_pop):
        cpu_level_easy_col = randint(0, game.cols - 1)
        cpu_level_easy_pop = randint(0, 1)
    return (cpu_level_easy_col, bool(cpu_level_easy_pop))


# create a sub-class that inherits from the Game-class
class simulate_game(Game):
    pass


# copy the game-board in order to simulat the moves
# without messing up the original game-board
def simulation(game):
    simulation_g = simulate_game(game.rows, game.cols, game.turn, game.wins)
    simulation_g.mat = np.copy(game.mat, 'F')
    return simulation_g


# during simlulation process of the computer-move module
# we do not want to alter the game.turn's value
# the rest is similar to the function apply_move
def simulate_apply_move(game, chosen_col, pop):
    if pop:
        for i in range(0, game.rows - 1):
            game.mat[i][chosen_col] = game.mat[i + 1][chosen_col]
        game.mat[game.rows - 1][chosen_col] = 0
    else:
        i = 0
        while game.mat[i][chosen_col] != 0:
            i += 1
        row = i
        game.mat[row][chosen_col] = game.turn
    return game


# PVC: medium level
# computer should be able to prevent winner from winning by doing one-step move
def computer_level_medium(game):
    indicator = 0
    # check whether computer can win
    # randomly generate the move
    for pop in range(0, 2):
        for col in range(game.cols):
            # check the validity
            if check_move(game, col, pop):
                # apply the move on the simulated game board
                simulate_game = simulation(game)
                simulate_game = simulate_apply_move(simulate_game, col, pop)
                # check if the move will lead to a win for computer
                if check_victory(simulate_game) == game.turn:
                    indicator = 1
                    return (col, bool(pop))
                else:
                    continue
    # check if player can win
    # update game.turn to make human player's turn
    update_game_turn(game)
    opponent_turn = game.turn
    for pop in range(0, 2):
        for col in range(game.cols):
            if check_move(game, col, pop):
                simulate_game = simulation(game)
                simulate_game = simulate_apply_move(simulate_game, col, pop)
                # check if the move will lead to a win for human player
                if check_victory(simulate_game) == opponent_turn:
                    # if the move will not pop out a block,i.e add on a block to the column
                    # computer will do that move
                    if not pop:
                        indicator = 1
                        update_game_turn(game)
                        return (col, bool(pop))
                    # the move includes poping out a bottom block
                    else:
                        # computer will seek an opportunity to stop human player from poping out the block
                        # e.g. popping out another block,if possible, to change the gameboard
                        game.turn = update_game_turn(game)
                        # flag is used to indicate whether computer founds a defensive move
                        flag = 1
                        simulate_game_pop = simulation(simulate_game)
                        # go through all possibe moves to find the defensive move
                        for i in range(simulate_game_pop.cols):
                            if check_move(simulate_game_pop, i, 0):
                                simulate_game_pop = simulate_apply_move(simulate_game_pop, i, 0)
                                # if apply that move will prevents the human player from winning the game
                                # computer will return that move
                                if check_victory(simulate_game_pop) != opponent_turn:
                                    flag = 0
                                    indicator = 1
                                    update_game_turn(game)
                                    return (i, bool(1))
                        # if there is no defensive move, computer will concede directly
                        if flag == 1:
                            print("YOU WIN THIS TIME!")
                            exit(0)
                else:
                    continue
    # adjust the game.turn back to make computer's turn
    update_game_turn(game)
    # if neither computer nor human player will win by applying a single move
    # evoke the PVC:easy-level
    if indicator == 0:
        (col, pop) = computer_level_easy(game)
        return (col, pop)


# PVC: difficult
# the basic idea is to assign scores to the appearance of n consecutive blocks

# count the number of occurence of the n-consecutive-blocks
def check_NO_of_consecutive_blocks(game, number_required):
    count = 0
    # check horizontal
    for i in range(game.rows):  # check rows
        signal = 0
        for j in range(game.cols):
            if game.mat[i][j] == game.turn:
                signal += 1
                if signal >= number_required:
                    count += 1
            else:
                signal = 0
    # check vertical
    for j in range(0, game.cols):
        signal = 0
        for i in range(0, game.rows):
            if game.mat[i][j] == game.turn:
                signal += 1
                if signal >= number_required:
                    count += 1
                else:
                    signal = 0

    # + digonal
    for i in range(0, game.rows - game.wins + 1):
        for j in range(0, game.cols - game.wins + 1):
            signal = 0
            for k in range(0, game.wins):
                if game.mat[i + k][j + k] == game.turn:
                    if signal >= number_required:
                        count += 1
                else:
                    signal = 0
    # - diagonal
    for i in range(game.wins - 1, game.rows):
        for j in range(0, game.cols - game.wins + 1):
            signal = 0
            for k in range(0, game.wins):
                if game.mat[i - k][j + k] == game.turn:
                    signal += 1
                    if signal >= number_required:
                        count += 1
                else:
                    signal = 0

    return count


def computer_level_difficult(game):
    # check whether there is winning condition: following will be the same as the upper part of medium-level
    for pop in range(0, 2):
        for col in range(game.cols):
            if check_move(game, col, pop):
                simulate_game = simulation(game)
                simulate_game = simulate_apply_move(simulate_game, col, pop)
                if check_victory(simulate_game) == game.turn:
                    return (col, bool(pop))
                else:
                    continue
    # check if player can win
    update_game_turn(game)
    opponent_turn = game.turn
    for pop in range(0, 2):
        for col in range(game.cols):
            if check_move(game, col, pop):
                simulate_game = simulation(game)
                simulate_game = simulate_apply_move(simulate_game, col, pop)
                if check_victory(simulate_game) == opponent_turn:
                    if not pop:
                        update_game_turn(game)
                        return (col, bool(pop))
                    else:
                        game.turn = update_game_turn(game)
                        flag = 1
                        simulate_game_pop = simulation(simulate_game)
                        for i in range(simulate_game_pop.cols):
                            if check_move(simulate_game_pop, i, 0):
                                simulate_game_pop = simulate_apply_move(simulate_game_pop, i, 0)
                                if check_victory(simulate_game_pop) != opponent_turn:
                                    flag = 0
                                    update_game_turn(game)
                                    return (i, bool(1))
                        if flag == 1:
                            print("YOU WIN THIS TIME!")
                            exit(0)
                else:
                    continue
    update_game_turn(game)

    # seek the best moves where no winning or lose conditions are met
    win_score = 10000
    move_list = []
    for pop in range(0, 2):
        for col in range(game.cols):
            if check_move(game, col, pop):
                simulate_game = simulation(game)
                simulate_game = simulate_apply_move(simulate_game, col, pop)
                score_sum = 0
                # calculate the score for each move
                for n in range(2, game.wins):
                    counts = check_NO_of_consecutive_blocks(simulate_game, n)
                    score_sum += counts * win_score / (10 ** (game.wins - n))
                move_list.append((score_sum, (col, bool(pop))))
    target_move = (0, (0, False))  # random initialization
    # find the move with the highest score
    for i in move_list:
        if i[0] > target_move[0]:
            target_move = i

    return target_move[1]


def computer_move(game, level):
    if level == 1:
        (col, pop) = computer_level_easy(game)
    if level == 2:
        (col, pop) = computer_level_medium(game)
    if level == 3:
        (col, pop) = computer_level_difficult(game)
    return (col, pop)


menu()
