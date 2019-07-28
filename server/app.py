from flask import Flask, request, jsonify
from flask_cors import CORS
from ttt.board import GameState, Player
from ttt.utils import board_from_chars, chars_from_board
from ttt.utils import winner_char
from ttt.agent import MinimaxAgent
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["JSON_SORT_KEYS"] = False
CORS(app)

@app.route('/')
def root():
    return "Hi! This is tic-tac-toe bot server!"

@app.route('/bot')
def bot():
    result = {"winner": None, "response": None, "valid": False}
    
    # 入力値チェック
    board = request.args["board"]
    if not board:
        result['message'] = "boardがありません"
        return jsonify(result)
    
    try:
        board = json.loads(board)
        board = board_from_chars(board)
    except:
        result['message'] = "boardの値が不正です"
        return jsonify(result)

    result["valid"] = True;

    # ゲーム開始
    game = GameState(board, Player.o, None)

    # 黒の手で勝負が決まっていた場合
    if game.is_over():
        result["winner"] = winner_char(game.winner())
        result["response"] = {
            "board": chars_from_board(board)
        }
        return jsonify(result)

    # 白の手番が行える場合
    bot = MinimaxAgent()
    move = bot.select_move(game)
    point = move.point
    game = game.apply_move(move)
    response = {
        "row": point.row - 1,
        "col": point.col - 1,
        "board": chars_from_board(game.board)
    }
    result["response"] = response

    # 白の手番で勝負が決まった場合
    if game.is_over():
        result["winner"] = winner_char(game.winner())

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=False)