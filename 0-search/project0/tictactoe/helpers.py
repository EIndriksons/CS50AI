import math

def win_combinations(n):
    """
    Return a List of possible win combination indexes
    """
    combinations = []

    # Rows
    for row in range(n):
        combinations.append([(row, cell) for cell in range(n)])

    # Columns
    for cell in range(n):
        combinations.append([(row, cell) for row in range(3)])

    # Diagonal top left to bottom left
    combinations.append([(cell, cell) for cell in range(n)])
    
    # Diagonal top right to bottom left
    combinations.append([(cell, n - 1 - cell) for cell in range(n)])

    return combinations


def is_winner(board, decorator):
    """
    Returns True if the Winner has decorated a possible Win condition
    """
    n = len(board)
    combinations = win_combinations(n)

    for combination in combinations:
        if all(board[row][cell] == decorator for row, cell in combination):
            return True
    return False