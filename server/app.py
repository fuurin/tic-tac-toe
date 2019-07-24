from flask import Flask, request, jsonify
from .ttt.board import GameState, Move, Point
from .ttt.types import Player
from .ttt.utils import CHAR_TO_STONE
from .ttt.utils import point_from_coords, board_array
from .ttt.agent import MinimaxAgent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["JSON_SORT_KEYS"] = False

game = None
bot = None



@app.route('/')
def init():
    result = {"first": None, "response": None, "valid": False}

    first = request.args.get('first') or "x"
    if first not in ["o", "x"]:
        return jsonify(result)
    result["first"] = first

    result["valid"] = True

    global game, bot
    game = GameState.new_game(first=CHAR_TO_STONE[first])
    bot = MinimaxAgent()

    # 相手のターンから開始のとき
    if first == "o":
        move = bot.select_move(game)
        game = game.apply_move(move)
        result["response"] = move.point

    result["board"] = board_array(game.board)

    return jsonify(result)



@app.route('/move')
def move():
    result = {"winner": None, "response": None, "valid": False}

    # 初期化済みチェック
    global game, bot
    if game is None or game.board is None or bot is None:
        result["message"] = "ゲームが開始されていません。"
        return jsonify(result)

    # 入力値チェック
    try:
        row = int(request.args.get('row'))
    except Exception as error:
        result["message"] = "行の入力値に問題があります。"
        return jsonify(result)
    
    try:
        col = int(request.args.get('col'))
    except Exception as error:
        result["message"] = "列の入力値に問題があります。"
        return jsonify(result)

    point = Point(row=row, col=col)

    # 有効打チェック
    if not game.board.is_on_grid(point):
        result["message"] = "盤上にあるマスを指定してください。"
        return jsonify(result)
    
    if game.board.get(point) is not None:
        result["message"] = "そのマスはすでに着手済みです．"
        return jsonify(result)


    # プレイヤーのターン
    if not game.is_over():
        move = Move(point)
        game = game.apply_move(move)
    else:
        result["winner"] = game.winner()
    
    # 相手のターン
    if not game.is_over():
        move = bot.select_move(game)
        game = game.apply_move(move)
        result["response"] = move.point
    else:
        result["winner"] = game.winner()

    result["valid"] = True
    result["board"] = board_array(game.board)

    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True)