from .types import Player, Point
from .board import Board

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

def chars_from_board(board):
    plane = []
    for row in range(1, board.num_rows + 1):
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))  # 全ての点の打石状況を確認
            line.append(STONE_TO_CHAR[stone])
        plane.append(line)
    return plane

def board_from_chars(charBoard):
    board = Board()
    
    for col in range(1, board.num_cols+ 1):
        for row in range(1, board.num_rows +1):
            char = charBoard[col-1][row-1]
            stone = CHAR_TO_STONE[char]
            point = Point(row=row, col=col)
            board.place(stone, point)

    return board