from flask import Flask, request, jsonify
from flask_cors import CORS
from .ttt.board import Board, GameState, Player, Move
from .ttt.utils import board_from_chars, chars_from_board, lt_to_lb
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

    result["valid"] = True;
    
    if game.is_over():
        if game.winner() == Player.o:
            winner = "o"
        elif game.winner() == Player.x:
            winner = "x"
        else:
            winner = "draw"
        result["winner"] = winner
    else:
        bot = MinimaxAgent()
        move = bot.select_move(game)
        game = game.apply_move(move)

        if game.is_over():
            if game.winner() == Player.o:
                winner = "o"
            elif game.winner() == Player.x:
                winner = "x"
            else:
                winner = "draw"
            result["winner"] = winner
        response = {
            "row": range(3,0,-1)[move.point.row-1],
            "col": move.point.col,
            "board": chars_from_board(game.board)
        }
        result["response"] = response

    return jsonify(result)



game = None
bot = None

@app.route("/")
def init():
    global game
    global bot
    game = GameState.new_game()
    bot = MinimaxAgent()

    return jsonify({
        "message": "initialized",
        "board": chars_from_board(game.board)
    })

@app.route("/move")
def move():
    global game
    global bot

    if not game.is_over():
        row = int(request.args["row"])
        col = int(request.args["col"])
        point = lt_to_lb(row, col)
        player_move = Move(point)
        game = game.apply_move(player_move)
    else:
        return jsonify({
            "message": "GAME OVER!, Winner: " + (game.winner() or "draw"),
            "last_move": (player_move.point.row, player_move.point.col),
            "board": chars_from_board(game.board)
        })
    
    if not game.is_over():
        enemy_move = bot.select_move(game)        
        game = game.apply_move(enemy_move)
    else:
        return jsonify({
            "message": "GAME OVER!, Winner: " + (game.winner() or "draw"),
            "last_move": (enemy_move.point.row, enemy_move.point.col),
            "board": chars_from_board(game.board)
        })

    return jsonify({
        "message": "continue game",
        "player_move": (player_move.point.row, player_move.point.col),
        "enemy_move": (enemy_move.point.row, enemy_move.point.col),
        "board": chars_from_board(game.board)
    })
    

if __name__ == "__main__":
    app.run(debug=True)