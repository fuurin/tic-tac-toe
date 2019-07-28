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

COLS = "ABC"

def board_from_chars(charBoard):
    board = Board()
    
    for row in range(board.num_rows):
        for col in range(board.num_cols):
            char = charBoard[row][col]
            stone = CHAR_TO_STONE[char]
            point = Point(row=range(3,0,-1)[row], col=col+1)
            board.place(stone, point)

    return board

def point_from_coords(coords):
    """ 人間の入力をBoardの座標に変換 ex. C3 -> (3, 3) """
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return Point(row=row, col=col)

def lt_to_lb(row, col):
    """ 左上オリジンの座標を左下オリジンのPointに変換
        ex. (row, col) = (0, 1) -> Point(3, 2)
    """
    col = col + 1
    row = range(3, 0, -1)[row]
    return Point(row=row, col=col)

def chars_from_board(board):
    plane = []
    for row in range(board.num_rows, 0, -1):
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        plane.append(line)
    return plane
