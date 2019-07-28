from .types import Player, Point
from .board import Board
import numpy as np

STONE_TO_CHAR = {
    None: '+',
    Player.x: 'x',
    Player.o: 'o',
}

CHAR_TO_STONE = {
    '+': None,
    'x': Player.x,
    'o': Player.o,
}

def winner_char(player):
    if player == Player.x:
        return "x"
    elif player == Player.o:
        return "o"
    else:
        return "draw"

def board_from_chars(char_board):
    board = Board()

    if np.array(char_board).shape != (3,3):
        raise ValueError
    
    for row in range(board.num_rows):
        for col in range(board.num_cols):
            
            char = char_board[row][col]
            if char not in CHAR_TO_STONE.keys():
                raise ValueError

            stone = CHAR_TO_STONE[char]
            point = Point(row=range(3,0,-1)[row], col=col+1)
            board.place(stone, point)

    return board

def chars_from_board(board):
    plane = []
    for row in range(board.num_rows, 0, -1):
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        plane.append(line)
    return plane
