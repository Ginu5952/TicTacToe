
# capsys is a fixture provided by pytest, a popular testing framework in Python. 
#This fixture captures the output to stdout and stderr during the execution of a test function.
#readouterr() is a method provided by the capsys fixture. It captures the output to stdout and stderr and returns a tuple containing two strings: 
#the captured output to stdout and stderr, respectively.
#.out is an attribute of the tuple returned by readouterr(), which represents the captured output to stdout.

#.rstrip() is a method that removes any trailing whitespace (spaces, tabs, newlines) from the string.

from src import board
from unittest.mock import patch
import pytest
from src.custom_ex import CellNotEmptyError,CellOutOfBoundError

def test_welcome_message(capsys):
    expected_output = 'WELCOME TO TIC TAC TOE'

    board.welcome_message()

    output = capsys.readouterr().out.rstrip() 
   
    assert output == expected_output

def test_player_give_your_name():
    player_number = 1

    with patch('src.board.input') as input_mock: # with -> context manager
        board.player_give_your_name(player_number)

        input_mock.assert_called_once_with(f'Player {player_number}, give your name: ') # mock has been called once

def test_display_empty_board():
    game_board = [None] * 9
    expected_board = """
-------------
| 1 | 2 | 3 |
-------------
| 4 | 5 | 6 |
-------------
| 7 | 8 | 9 |
-------------
"""
    default_board = board.display_board(game_board)

    assert default_board == expected_board

def test_update_board_pass():
    # Arrange
    game_board = [None] * 9
    cell = 2
    player_number = 1    
    expected_board = [None,"X",*[None]*7]  # unpack None


    # Act
    updated_board = board.update_board(game_board,cell,player_number)

    # Assert
    assert updated_board == expected_board

def test_update_board_occupied_cell():
    # Arrange
    game_board = [None,'X','O',None,'X',None,None,None,None]
    cell = 2
    player_number = 2

    with pytest.raises(CellNotEmptyError):
        board.update_board(game_board,cell,player_number)

def test_update_board_out_of_bound_cell():
    # Arrange
    game_board = [None] * 9
    cell = 20
    player_number = 1
    expected_error_msg = 'Cell out of boud'

    # Act/Assert
    with pytest.raises(CellOutOfBoundError) as err:
        board.update_board(game_board,cell,player_number)  
        print('mkljhg') 
        assert err.msg == expected_error_msg   

# TODO: test all the winning patterns
@pytest.mark.parametrize(
        'game_board,player_number,is_winner',
        [
            (['X','X','X','O','O',None,None,None,None],1,True),
            (['X',None,'X','O','O','O',None,None,None],2,True)
        ]
)
def test_is_winner_true(game_board,player_number,is_winner):


    #Act/ Assert
    assert board.is_winner(game_board,player_number) == is_winner            

# TODO: use parameterize to check many failing patterns
def test_is_winner_false():
    game_board = ['X','O','X','O',None,None,None,None,None]
    player_number = 1

    is_winner = board.is_winner(game_board,player_number)

    assert is_winner is False


