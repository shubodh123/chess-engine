# Piece types (these go in the lower 3 bits)
EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6
# Colors (these use bit 3, worth 8)
WHITE = 0
BLACK = 8

# combined piece code
WHITE_PAWN = PAWN | WHITE       # 1 | 0 = 1  
WHITE_KNIGHT = KNIGHT | WHITE   # 2 | 0 = 2
WHITE_BISHOP = BISHOP | WHITE   # 3 | 0 = 3
WHITE_ROOK = ROOK | WHITE       # 4 | 0 = 4
WHITE_QUEEN = QUEEN | WHITE     # 5 | 0 = 5
WHITE_KING = KING | WHITE       # 6 | 0 = 6

BLACK_PAWN = PAWN | BLACK       # 1 | 8 = 9
BLACK_KNIGHT = KNIGHT | BLACK   # 2 | 8 = 10
BLACK_BISHOP = BISHOP | BLACK   # 3 | 8 = 11
BLACK_ROOK = ROOK | BLACK       # 4 | 8 = 12
BLACK_QUEEN = QUEEN | BLACK     # 5 | 8 = 13
BLACK_KING = KING | BLACK       # 6 | 8 = 14

# Display characters
PIECE_SYMBOLS = {
    EMPTY: '.',
    WHITE_PAWN: 'P',
    WHITE_KNIGHT: 'N',
    WHITE_BISHOP: 'B',
    WHITE_ROOK: 'R',
    WHITE_QUEEN: 'Q',
    WHITE_KING: 'K',
    BLACK_PAWN: 'p',
    BLACK_KNIGHT: 'n',
    BLACK_BISHOP: 'b',
    BLACK_ROOK: 'r',
    BLACK_QUEEN: 'q',
    BLACK_KING: 'k',
}