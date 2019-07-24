import enum, random

class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3

def reverse_game_result(result):
    if result == GameResult.loss:
        return GameResult.win
    if result == GameResult.win:
        return GameResult.loss
    return result

def best_result(game_state):
    
    # 勝敗が付いている場合，自分の勝敗結果を返す(再帰の最後)
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return GameResult.win
        elif game_state.winner() is None:
            return GameResult.draw
        else:
            return GameResult.loss
    
    best_result_so_far = GameResult.loss
    opponent = game_state.next_player.other

    # 全てのありうる手で，最も自分にとって良い結果を返す
    for candidate_move in game_state.legal_moves():
        
        # 自分が手を打った後，
        next_state = game_state.apply_move(candidate_move)
        
        # 相手の最善結果を予測
        opponent_best_result = best_result(next_state)
        
        # 相手の最善結果の逆が，その手による我々の結果になる
        our_result = reverse_game_result(opponent_best_result)
        
        # この手がより良い結果に結びつくならば，それをここまでの最善結果とする
        if our_result.value > best_result_so_far.value:
            best_result_so_far = our_result
    
    return best_result_so_far

class MinimaxAgent():
    
    # 最善の手順を返す
    def select_move(self, game_state):
        winning_moves = []
        draw_moves = []
        losing_moves = []
        
        # 全てのありうる手を，最善の結果ごとに記録していく
        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            
            # その手を打った時，相手の最善の結果の逆が自分の結果になる
            opponent_best_outcome = best_result(next_state)
            our_best_outcome = reverse_game_result(opponent_best_outcome)
            
            # 相手が最善の手を尽くしても自分が勝つような手を欲する
            if our_best_outcome == GameResult.win:
                winning_moves.append(possible_move)
            elif our_best_outcome == GameResult.draw:
                draw_moves.append(possible_move)
            else:
                losing_moves.append(possible_move)
        
        # 記録した手から最善の手を選んで返す
        if winning_moves:
            return random.choice(winning_moves)
        if draw_moves:
            return random.choice(draw_moves)
        return random.choice(losing_moves)