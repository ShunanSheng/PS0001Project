
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
    if pop:
        if game.mat[0][chosen_col] == game.turn:
            return True
        else:
            return False
    else:
        if game.mat[game.rows-1][chosen_col]==0:
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
        for i in range(0,game.rows-1):
            game.mat[i][chosen_col] = game.mat[i+1][chosen_col]
        game.mat[game.rows-1][chosen_col] = 0
    else:
        i=0
        while game.mat[i][chosen_col]!=0:
            i +=1
        row=i
            # print(i)
        game.mat[row][chosen_col] = game.turn
    update_game_turn(game)
    return game


def check_victory(game): # how to define draw or pass on

    # check horizontal condition
    for player in range(1,3):
        # print(piece)
        signal = 0
        for i in range(game.rows):  # check rows
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
        for j in range(0, game.cols ):
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
        for i in range(game.wins - 1, game.rows):  # check rows
            for j in range(0,game.cols-game.wins+1):
                for k in range(0, game.wins):
                    if game.mat[i - k][j + k] == player:
                        signal += 1
                        # print(signal)
                        if signal >= game.wins:
                            return player
                    else:
                        signal = 0
        # print("+ diagonal check done")


    for i in range(game.rows):
        for j in range(game.cols):
            if game.mat[i][j]==0:
                return 0
    return 3




def display_board(game):
    for i in range(game.rows-1,-1,-1):
        for j in range(game.cols):
            print(int(game.mat[i][j]),end=' ')
        print()


def choose_col(game):#Changed by ZSZ
        print('Player ',game.turn,"please choose a column to drop the piece (from 1 to ", game.cols, '):\n')
        chosen_col=input()
        while not (chosen_col.isdigit()==True and int(chosen_col)<=game.cols):
            print('Your input value is invalid! Please enter again')
            chosen_col = input()
        else:
            chosen_col=int(chosen_col)-1
        return chosen_col
# Modified Oct 29


def choose_add_on_method(game):
    print('Please choose the way to add the piece (1 for pop out, 0 for add on):\n')
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
    # print(victory_condition)
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
        if mode<1 or mode >3:
            print('Invalid input!')
            mode=int(input('Enter the diffculty level!(easy:1,medium:2,difficult:3)'))
    else:
        print("Invalid input!")
        mode= input('PvP or PvC?:Please enter 1 for PvP mode, 2 for PvC mode')
    return mode
# Modified Oct 29

def menu():
    game = Game()
    game.rows = input("How many rows?")
    while not (game.rows.isdigit()==True and int(game.rows)>=3):
        print('Your input value is invalid! Please enter again')
        game.rows = input()
    else: game.rows=int(game.rows)
    game.cols = input("How many columns?:")
    while not (game.cols.isdigit()==True and int(game.cols)>=3):
        print('Your input value is invalid! Please enter again')
        game.cols = input()
    else: game.cols=int(game.cols)
    game.wins = input("How many wins:")
    while not (game.wins.isdigit()==True and int(game.wins)<=game.rows):
        print('Your input value is invalid! Please enter again')
        game.wins = input()
    else: game.wins=int(game.wins)

# Modified Oct 29
    game.turn = randint(1, 2)
    game.mat = np.zeros((game.rows, game.cols))
    mode = add_mode()
    game_over = False

    while not game_over:
        if game.turn == 1:
            if mode==0:
                human_move(game)
                display_board(game)
            if mode!=0:
                (col,pop)=computer_move(game,mode)
                game=apply_move(game,col,pop)
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

def computer_level_easy(game):
    cpu_level_easy_col = randint(0, game.cols - 1)
    cpu_level_easy_pop = randint(0, 1)
    try_to_think()
    while not check_move(game, cpu_level_easy_col, cpu_level_easy_pop):
        cpu_level_easy_col = randint(0, game.cols - 1)
        cpu_level_easy_pop = randint(0, 1)
    return (cpu_level_easy_col,bool(cpu_level_easy_pop))

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

def simulate_apply_move(game,chosen_col,pop):
    if pop:  # 1 for pop out;0 for add on
        for i in range(0,game.rows-1):
            game.mat[i][chosen_col] = game.mat[i+1][chosen_col]
        game.mat[game.rows-1][chosen_col] = 0
    else:
        i=0
        while game.mat[i][chosen_col]!=0:
            i +=1
        row=i
            # print(i)
        game.mat[row][chosen_col] = game.turn
    return game





def computer_level_medium(game):
    indicator=0
    #check whether computer can win
    for pop in range(0,2):
        for col in range(game.cols):
            if check_move(game,col,pop):
                simulate_game = simulation(game)
                simulate_apply_move(simulate_game,col,pop)
                if check_victory(simulate_game)==1:
                    indicator=1
                    try_to_think()
                    return (col,bool(pop))
                else:
                    continue
    #check if player can win...bug 1: pop, temporary attempt, copy the board and try the possible pop out moves
    game.turn=2
    for pop in range(0,2):
        for col in range(game.cols):
            if check_move(game,col,pop):
                simulate_game=simulation(game)
                simulate_game=simulate_apply_move(simulate_game,col,pop)
                if check_victory(simulate_game)==2:
                    if not pop:
                        indicator = 1
                        try_to_think()
                        game.turn = 1
                        return (col,bool(pop))
                    else:
                        game.turn=1
                        flag=1
                        simulate_game_pop=simulation(simulate_game)
                        try_to_think()
                        for i in range(simulate_game_pop.cols):
                            if check_move(simulate_game_pop,i,0):
                                simulate_game_pop = simulate_apply_move(simulate_game_pop,i,0)
                                if check_victory(simulate_game_pop)!=2:
                                    flag=0
                                    indicator=1
                                    return (i,bool(0))
                        if flag==1:
                            print("YOU WIN THIS TIME!")
                            exit(0)
                else:
                    continue
    game.turn=1

    if indicator==0:
        (col,pop)=computer_level_easy(game)
        return (col,pop)



def computer_level_difficult(game):
    pass

def computer_move(game,level):
    if level==1:
        (col,pop)=computer_level_easy(game)
    if level==2:
        (col,pop)=computer_level_medium(game)
    if level==3:
        (col,pop)=computer_level_difficult(game)
    return (col,pop)
