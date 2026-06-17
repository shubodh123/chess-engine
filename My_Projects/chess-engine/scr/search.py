"""
Search algorithm - Minimax with alpha-beta pruning.
"""
from evaluation import evaluate
from constants import WHITE, BLACK


# Simple move ordering - captures first (improves pruning)
def order_moves(board, moves):
    captures = []
    quiet = []
    for move in moves:
        from_sq, to_sq = move
        if board.squares[to_sq] != 0:  # Capturing something
            captures.append(move)
        else:
            quiet.append(move)
    return captures + quiet


def minimax(board, depth, alpha, beta, maximizing):
    """Minimax with alpha-beta pruning."""
    if depth == 0:
        return evaluate(board), None
    
    color = WHITE if maximizing else BLACK
    moves = board.get_legal_moves(color)
    moves = order_moves(board, moves)
    
    if not moves:
        # Checkmate or stalemate
        if board.is_in_check(color):
            return (-99999 if maximizing else 99999), None  # Checkmate
        return 0, None  # Stalemate
    
    best_move = moves[0]
    
    if maximizing:
        max_eval = -99999
        for move in moves:
            from_sq, to_sq = move
            # Make move
            captured = board.squares[to_sq]
            board.squares[to_sq] = board.squares[from_sq]
            board.squares[from_sq] = 0
            board.current_player = BLACK
            
            eval_score, _ = minimax(board, depth - 1, alpha, beta, False)
            
            # Undo move
            board.squares[from_sq] = board.squares[to_sq]
            board.squares[to_sq] = captured
            board.current_player = WHITE
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Prune
        
        return max_eval, best_move
    
    else:
        min_eval = 99999
        for move in moves:
            from_sq, to_sq = move
            captured = board.squares[to_sq]
            board.squares[to_sq] = board.squares[from_sq]
            board.squares[from_sq] = 0
            board.current_player = WHITE
            
            eval_score, _ = minimax(board, depth - 1, alpha, beta, True)
            
            # Undo move
            board.squares[from_sq] = board.squares[to_sq]
            board.squares[to_sq] = captured
            board.current_player = BLACK
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Prune
        
        return min_eval, best_move


def get_best_move(board, depth=3):
    """Get the best move for the current player."""
    maximizing = board.current_player == WHITE
    score, move = minimax(board, depth, -99999, 99999, maximizing)
    return move