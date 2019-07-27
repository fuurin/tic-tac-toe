from flask import Flask, request, jsonify
from flask_cors import CORS
from .ttt.board import Board, GameState, Move, Point
from .ttt.types import Player
from .ttt.utils import CHAR_TO_STONE, board_from_chars
from .ttt.utils import point_from_coords, board_array
from .ttt.agent import MinimaxAgent
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["JSON_SORT_KEYS"] = False
CORS(app)

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
        response = {"row": move.point.row, "col": move.point.col}
        result["response"] = response

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
    
    # import pdb; pdb.set_trace()
    
    if game.board.get(point) is not None:
        result["message"] = "そのマスはすでに着手済みです．"
        result["board"] = board_array(game.board)
        result["point"] = {"row": point.row, "col": point.col}
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
        response = {"row": move.point.row, "col": move.point.col}
        result["response"] = response
    else:
        result["winner"] = game.winner()

    result["valid"] = True
    result["board"] = board_array(game.board)

    return jsonify(result)

@app.route("/bot")
def bot():
    result = {"winner": None, "response": None, "valid": False}
    
    board = request.args["board"]
    if not board:
        result['message'] = "boardがありません"
        return jsonify(result)
    
    board = json.loads(board)
    result["response"] = {"board": board}

    board = board_from_chars(board)    
    game = GameState(board, Player.o, None)

    if game.is_over():
        result["winner"] = game.winner()
    else:
        bot = MinimaxAgent()
        move = bot.select_move(game)
        game.apply_move(move)
        if game.is_over():
            result["winner"] = game.winner()
        response = {
            "row": move.point.row, 
            "col": move.point.col,
            "board": board_array(game.board)
        }
        result["response"] = response

    return jsonify(result)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}, 404)

if __name__ == "__main__":
    # debug=Falseにすると意図しないアクセスが発生
    # おそらくキャッシュ読み込みがかかる
    # OC用なのでとりあえずdebug=Trueのままにしよう
    app.run(debug=True)