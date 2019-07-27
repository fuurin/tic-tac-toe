from flask import Flask, request, jsonify
from flask_cors import CORS
from .ttt.board import Board, GameState, Player
from .ttt.utils import board_from_chars, chars_from_board
from .ttt.agent import MinimaxAgent
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["JSON_SORT_KEYS"] = False
CORS(app)

@app.route('/bot')
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
        game = game.apply_move(move)
        if game.is_over():
            result["winner"] = game.winner()
        response = {
            "row": move.point.row, 
            "col": move.point.col,
            "board": chars_from_board(game.board)
        }
        result["response"] = response

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)