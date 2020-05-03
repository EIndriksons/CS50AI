"""
Tic Tac Toe Player
"""

import math
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
    raise NotImplementedError


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
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
