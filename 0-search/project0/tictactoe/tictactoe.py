"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from helpers import is_winner

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    XTurns = 0
    OTurns = 0

    # Iterate through the board and count all turns
    for row in board:
        for cell in row:
            if cell == 'X':
                XTurns += 1
            if cell == 'O':
                OTurns += 1
    
    # Return the next player turn
    if XTurns > OTurns:
        return "O"
    else:
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    # Iterate through the board and count all EMPTY fields
    for row in board:
        for cell in row:
            if cell == EMPTY:
                actions.add((row, cell))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # Check for if the action is valid (i.e. the action cell is empty)
    if board[i][j] != EMPTY:
        raise NameError('Not a Valid Action!')

    # Check whose player's turn it is
    current_player = player(board)

    # Deep copy a board as we shouldn't change the original board as it will be used in Minimax
    boardcopy = deepcopy(board)

    # Update the copy of the board
    boardcopy[i][j] = current_player
    return boardcopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if is_winner(board, "X"):
        return "X"
    elif is_winner(board, "O"):
        return "O"
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == "X" or winner(board) == "O" or len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    raise NotImplementedError

    
