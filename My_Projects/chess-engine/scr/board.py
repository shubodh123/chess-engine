from constants import (
    EMPTY,
    WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK, WHITE_QUEEN, WHITE_KING,
    BLACK_PAWN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK, BLACK_QUEEN, BLACK_KING,
    PIECE_SYMBOLS, WHITE, BLACK
)

from move_generator import MoveGenerator

class Board:
    def __init__(self):
        # self.squares = [EMPTY] * 64    # creates list of 64 zeros
        # self.current_player = WHITE     # white moves first
        # self._setup_starting_position()
        self.squares = [EMPTY] * 64
        self.current_player = WHITE
        self.last_move = None 
        self.move_gen = MoveGenerator()  # Add this
        self._setup_starting_position()
    
    def _setup_starting_position(self):
        # White's back rank (rank 1, indices 0-7)
        self.squares[0:8] = [
            WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN,
            WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK
        ]
        
        # White's pawns (rank 2, indices 8-15)
        self.squares[8:16] = [WHITE_PAWN] * 8
        
        # Black's pawns (rank 7, indices 48-55)
        self.squares[48:56] = [BLACK_PAWN] * 8
        
        # Black's back rank (rank 8, indices 56-63)
        self.squares[56:64] = [
            BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN,
            BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK
        ]
    
    def display(self):
        print("\n  +------------------------+")
        # Loop from rank 8 down to rank 1 (top to bottom of screen)
        for rank in range(7, -1, -1):
            print(f"{rank + 1} |", end=" ")
            for file in range(8):
                square = rank * 8 + file
                piece = self.squares[square]
                print(f"{PIECE_SYMBOLS[piece]}", end=" ")
            print("|")
        print("  +------------------------+")
        print("    a b c d e f g h")
        print(f"\n  {'White' if self.current_player == WHITE else 'Black'} to move")
    
    def make_move(self, from_square, to_square):

        """Execute a move on the board."""
        piece = self.squares[from_square]
        self.squares[to_square] = piece
        self.squares[from_square] = EMPTY
        
        # Switch turns
        self.current_player = BLACK if self.current_player == WHITE else WHITE
    
    def is_square_attacked(self, square, attacker_color):

        """Check if a square is attacked by any piece of attacker_color."""
        # Quick and dirty: generate all moves for attacker, see if square is a target
        gen = MoveGenerator()
        all_moves = gen.get_all_moves(self, attacker_color)
        for _, target in all_moves:
            if target == square:
                return True
        return False
    
    def make_move(self, from_square, to_square):
        """Execute a move on the board."""
        self.squares[to_square] = self.squares[from_square]
        self.squares[from_square] = EMPTY
        self.current_player = BLACK if self.current_player == WHITE else WHITE
    
    def is_in_check(self, color):
        """Check if the given color's king is under attack."""
        # Find the king
        king_square = None
        king_piece = WHITE_KING if color == WHITE else BLACK_KING
        for sq in range(64):
            if self.squares[sq] == king_piece:
                king_square = sq
                break
        
        enemy_color = BLACK if color == WHITE else WHITE
        return self.is_square_attacked(king_square, enemy_color)
    
    def is_square_attacked(self, square, attacker_color):
        """Check if a square is attacked by attacker's pieces."""
        enemy_moves = self.move_gen.get_all_moves(self, attacker_color)
        for _, target in enemy_moves:
            if target == square:
                return True
        return False
    
    def get_legal_moves(self, color):
        """Get only moves that don't leave own king in check."""
        from special_moves import get_castling_moves, get_en_passant_moves
        
        legal = []
        pseudo_legal = self.move_gen.get_all_moves(self, color)
        
        # Add special moves
        get_castling_moves(self, color, pseudo_legal)
        get_en_passant_moves(self, color, self.last_move, pseudo_legal)
        
        for move in pseudo_legal:
            from_sq, to_sq = move
            
            # Make move on a copy
            captured = self.squares[to_sq]
            self.squares[to_sq] = self.squares[from_sq]
            self.squares[from_sq] = EMPTY
            
            # If our king is still safe, it's legal
            if not self.is_in_check(color):
                legal.append(move)
            
            # Undo move
            self.squares[from_sq] = self.squares[to_sq]
            self.squares[to_sq] = captured
        
        return legal
