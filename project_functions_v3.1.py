
import numpy as np
from random import randint
import time


class Game:
    def __init__(self,rows=6,cols=7,turn=1,wins=4):
        self.rows=rows
        self.cols=cols
        self.turn=turn
        self.wins=wins
        self.mat=None

    def create_board(self):
        return np.zeros((self.rows,self.cols))



def check_move(game,chosen_col, pop):  # needs inspectation
    if pop==0:
        if game.mat[game.rows - 1][chosen_col] == game.turn:
            return True
        else:
            return False
    else:
        if game.mat[0][chosen_col]==0:
            return True
        else:
            return False



def apply_move(game, chosen_col, pop):
    if pop==0:  # 0 for pop out;1 for add on
        for i in range(game.rows-1,0,-1):
            game.mat[i][chosen_col] = game.mat[i-1][chosen_col]
        game.mat[0][chosen_col] = 0
    else:
        for i in range(game.rows):
            if game.mat[i][chosen_col] == 0:
                row = i
            # print(i)
        game.mat[row][chosen_col] = game.turn

    return game


def check_victory(game): # how to define draw or pass on

    # check horizontal condition
    for piece in range(1,game.turn+1):
        # print(piece)
        signal = 0
        for i in range(game.rows):  # check rows
            for j in range(game.cols):
                if game.mat[i][j] == piece:
                    signal += 1
                    # print(signal)
                    if signal >= game.wins:
                        win_player = piece
                        return win_player
                else:
                    signal = 0

        # print("row check done")

        # check vertical condition
        for j in range(0, game.cols ):
            for i in range(0, game.rows):
                if game.mat[i][j] == piece:
                    signal += 1
                    # print(signal)
                    if signal >= game.wins:
                        win_player = piece
                        return win_player
                else:
                    signal = 0
        # print("col check done")


        # check nagative sloped diagonals
        for i in range(0, game.rows - game.wins + 1):  # check rows
            for j in range(0, game.cols - game.wins + 1):
                for k in range(0, game.wins):
                    if game.mat[i + k][j + k] == piece:
                        signal += 1
                        # print(signal)
                        if signal >= game.wins:
                            win_player = piece
                            return win_player
                    else:
                        signal = 0
        # print("- diagonal check done")

        # check positive sloped digonals
        for i in range(game.wins - 1, game.rows):  # check rows
            for j in range(0,game.cols-game.wins+1):
                for k in range(0, game.wins):
                    if game.mat[i - k][j + k] == piece:
                        signal += 1
                        # print(signal)
                        if signal >= game.wins:
                            win_player = piece
                            return win_player
                    else:
                        signal = 0
        # print("+ diagonal check done")


    for i in range(game.rows):
        for j in range(game.cols):
            if game.mat[i][j]==0:
                return 0
    return 3




def display_board(game):
    for i in range(game.rows):
        for j in range(game.cols):
            print(int(game.mat[i][j]),end=' ')
        print()

def choose_col(game):
    print('Player ',game.turn,"please choose a column to drop the piece (from 0 to ", game.cols-1, '):\n')
    while True:
        chosen_col=int(input())
        if 0<=chosen_col<game.cols:
            break
        else:
            print("Invalid column chosen!")
            chosen_col = int(input())
    return chosen_col


def choose_add_on_method(game):
    print('Please choose the way to add the piece (0 for pop out, 1 for add on):\n')
    while True:
        pop=int(input())
        if pop==0 or pop==1:
            break
        else:
            print("Invalid move!")
    return pop


def human_move(game):
    col = choose_col(game)
    pop = choose_add_on_method(game)
    if check_move(game, col, pop):
        game = apply_move(game, col, pop)


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

def update_game_turn(game):
    game.turn += 1
    if game.turn % 2 == 0:
        game.turn = 2
    else:
        game.turn = 1
    return game.turn

def add_mode():
    mode = input('PvP or PvC?:')
    if mode == 'PvP':
        mode = 0
    elif mode == 'PvC':
        print('Which difficulty level do you choose?(easy:1,medium:2,difficult:3):')
        mode = int(input())
        if mode<1 or mode >3:
            print('Invalid input!')
            mode=int(input('Enter the difficulty level!'))
    else:
        print("Invalid input!")
        mode= input('PvP or PvC?:')
    return mode

def menu():
    game = Game()
    try:
        game.rows = int(input("How many rows?"))
        game.cols = int(input("How many columns?:"))
        game.turn = randint(1, 2)  # 1 for player 1 start first
        game.wins = int(input("How many wins:"))
        if game.wins > game.rows or game.wins > game.cols:
            print('Invalid input')
            game.wins = int(input("How many wins:"))
        game.mat = np.zeros((game.rows, game.cols))
        mode = add_mode()
        game_over = False
    except ValueError:
        print("Invalid input!")

    while not game_over:
        if game.turn == 1:
            human_move(game)
            display_board(game)
            condition = check_and_print_winner(game)
            if condition != 0:
                game_over = True
            game.turn = update_game_turn(game)
        else:
            if mode==0:
                human_move(game)
                display_board(game)
            if mode!=0:
                computer_move(game,mode)
                display_board(game)
            condition = check_and_print_winner(game)
            if condition != 0:
                game_over = True
            game.turn = update_game_turn(game)

def try_to_think():
    print("CPU will make the move!")
    print("CPU is thinking...")
    time.sleep(3)

def computer_level_easy(game):
    cpu_level_easy_col = randint(0, game.cols - 1)
    cpu_level_easy_pop = randint(0, 1)
    try_to_think()
    while not check_move(game, cpu_level_easy_col, cpu_level_easy_pop):
        cpu_level_easy_col = randint(0, game.cols - 1)
        cpu_level_easy_pop = randint(0, 1)
    apply_move(game,cpu_level_easy_col,cpu_level_easy_pop)

class simulate_game(Game):
    pass
    # def __init__(self):
    #     self.rows=Game.rows
    #     self.cols=Game.cols
    #     self.turn =Game.turn
    #     self.wins =Game.wins
    #     self.mat = None

def simulation(game):
    simulation_g = simulate_game(game.rows,game.cols,game.turn,game.wins)
    simulation_g.mat=np.copy(game.mat,'F')
    return simulation_g


def computer_level_medium(game):
    indicator=0
    #check whether computer can win
    for pop in range(0,2):
        for col in range(game.cols):
            if check_move(game,col,pop):
                simulate_game = simulation(game)
                apply_move(simulate_game,col,pop)
                if check_victory(simulate_game)==2:
                    must_move_col = col
                    must_move_pop = pop
                    indicator=1
                    try_to_think()
                    apply_move(game,must_move_col,must_move_pop)
                else:
                    continue
    #check if player can win
    game.turn=1
    for pop in range(0,2):
        for col in range(game.cols):
            if check_move(game,col,pop):
                simulate_game=simulation(game)
                apply_move(simulate_game,col,pop)
                if check_victory(simulate_game)==1:
                    must_move_col = col
                    must_move_pop = pop
                    indicator=1
                    try_to_think()
                    game.turn=2
                    apply_move(game,must_move_col,must_move_pop)
                else:
                    continue
    game.turn=2

    if indicator==0:
        computer_level_easy(game)



def computer_level_difficult(game):
    pass

def computer_move(game,level):
    if level==1:
        computer_level_easy(game)
    if level==2:
        computer_level_medium(game)
    if level==3:
        computer_level_difficult(game)


menu()














