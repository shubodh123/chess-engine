"""
Position evaluation - scores the board from white's perspective.
Positive = good for white, negative = good for black.
"""
from constants import EMPTY, WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING


# Standard piece values
PIECE_VALUES = {
    PAWN: 100,
    KNIGHT: 320,
    BISHOP: 330,
    ROOK: 500,
    QUEEN: 900,
    KING: 20000  # King is priceless
}


def evaluate(board):
    """Evaluate the position. Positive = white advantage."""
    score = 0
    
    for square in range(64):
        piece = board.squares[square]
        if piece == EMPTY:
            continue
        
        piece_type = piece & 7   # Lower 3 bits = type
        piece_color = piece & 8  # Bit 3 = color (0=white, 8=black)
        value = PIECE_VALUES[piece_type]
        
        if piece_color == WHITE:
            score += value
        else:
            score -= value
    
    return score