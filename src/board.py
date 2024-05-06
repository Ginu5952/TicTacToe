# Colors

RESET = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
ORANGE = '\033[38;5;208m'
PINK = '\033[38;5;206m'

# Font Styles

BOLD = '\033[1m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
     


from src.custom_ex import CellNotEmptyError,CellOutOfBoundError

def welcome_message():
    print(PURPLE + ITALIC + f'WELCOME TO TIC TAC TOE' + RESET)

def player_give_your_name(player_number):
    player_name = input(ORANGE + f'Player {player_number}, give your name: ')    
    return player_name

def display_board(game_board:list[None | str]):
   # TODO :look for a better solution
   cell1,cell2,cell3,cell4,cell5,cell6,cell7,cell8,cell9 = game_board   
   return f"""
-------------
| {cell1 if cell1 else 1} | {cell2 if cell2 else 2} | {cell3 if cell3 else 3} |
-------------
| {cell4 if cell4 else 4} | {cell5 if cell5 else 5} | {cell6 if cell6 else 6} |
-------------
| {cell7 if cell7 else 7} | {cell8 if cell8 else 8} | {cell9 if cell9 else 9} |
-------------
"""

def update_board(game_board: list[None | str], cell:int, player_number:int):

    if cell not in range(1,len(game_board) + 1): # range(1,10)
        raise CellOutOfBoundError()
    
    if game_board[cell-1] is not None:
        raise CellNotEmptyError('Cell is not empty')
    
    # select the right character ('x','o')
    mark = ('X','O')[player_number-1]  # 1 - 1 = 0 -> X  computer -> O

    # update board with mark
    game_board[cell-1] = mark  
     

    return game_board

def is_winner(game_board:list[None | str], player_number:int) -> bool:
    # TODO:come up with a better solution.
    winning_patterns:list[list[int]] = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8], 
        [2,4,6],
    ]

    mark = ('X','O')[player_number-1]

    for i,j,k in winning_patterns:
        if (game_board[i], game_board[j],game_board[k]) == (mark,) * 3:
            return True
    return False    

# TODO:Test this function
def is_board_full(game_board:list[None | str]) -> bool:
    return None not in game_board