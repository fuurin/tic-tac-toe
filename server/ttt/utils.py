from .types import Player, Point

COLS = 'ABCDEFGHIJKLMNOPQRST'
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


def print_move(player, move):
    """ 着手の内容を表示．打石は 'x C3' のように表示 """
    move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('%s %s' % (player, move_str))


def print_board(board):
    """ 盤面全体の状況を表示 """
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""  # 二桁の行番号になったときのための空白
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))  # 全ての点の打石状況を確認
            line.append(STONE_TO_CHAR[stone])
        print('%s%d %s' % (bump, row, ''.join(line)))  # 空白，行番号，行の石
    print('    ' + ''.join(COLS[:board.num_cols]))  # 列記号，ABCD...

def board_array(board):
    plane = []
    for row in range(1, board.num_rows + 1):
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))  # 全ての点の打石状況を確認
            line.append(STONE_TO_CHAR[stone])
        plane.append(line)
    return plane

def point_from_coords(coords):
    """ 人間の入力をBoardの座標に変換 ex. C3 -> (3, 3) """
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return Point(row=row, col=col)
