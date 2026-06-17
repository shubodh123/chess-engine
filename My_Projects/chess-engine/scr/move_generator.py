"""
Move generation for all chess pieces.
Uses pre-computed move tables for efficiency.
"""
from constants import (
    EMPTY, WHITE, BLACK,
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING,
    WHITE_PAWN, BLACK_PAWN, KING
)


class MoveGenerator:
    def __init__(self):
        # Pre-compute all knight moves for every square
        self.knight_moves = self._precompute_knight_moves()
        # Pre-compute all king moves
        self.king_moves = self._precompute_king_moves()
    
    def _precompute_knight_moves(self):
        """Calculate all 8 knight jumps from each square, filter out off-board ones."""
        moves = [[] for _ in range(64)]  # 64 empty lists
        
        # All 8 possible knight offsets (rank_change, file_change)
        knight_offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for square in range(64):
            rank = square // 8  # Integer division gives rank (0-7)
            file = square % 8   # Modulo gives file (0-7)
            
            for rank_offset, file_offset in knight_offsets:
                new_rank = rank + rank_offset
                new_file = file + file_offset
                
                # Check if the new position is on the board
                if 0 <= new_rank < 8 and 0 <= new_file < 8:
                    target_square = new_rank * 8 + new_file
                    moves[square].append(target_square)
        
        return moves
    
    def _precompute_king_moves(self):
        """Calculate all 8 king moves from each square."""
        moves = [[] for _ in range(64)]
        
        # All 8 directions (including diagonals)
        king_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for square in range(64):
            rank = square // 8
            file = square % 8
            
            for rank_offset, file_offset in king_offsets:
                new_rank = rank + rank_offset
                new_file = file + file_offset
                
                if 0 <= new_rank < 8 and 0 <= new_file < 8:
                    target_square = new_rank * 8 + new_file
                    moves[square].append(target_square)
        
        return moves
    
    def get_knight_moves(self, square, board, color):
        """Get legal knight moves from a square."""
        moves = []
        # Get enemy color
        enemy_color = BLACK if color == WHITE else WHITE
        
        for target in self.knight_moves[square]:
            piece = board.squares[target]
            # Can move if square is empty or has enemy piece
            if piece == EMPTY or (piece & 8) == enemy_color:
                moves.append(target)
        
        return moves
    
    def get_king_moves(self, square, board, color):
        """Get legal king moves (excluding castling for now)."""
        moves = []
        enemy_color = BLACK if color == WHITE else WHITE
        
        for target in self.king_moves[square]:
            piece = board.squares[target]
            if piece == EMPTY or (piece & 8) == enemy_color:
                moves.append(target)
        
        return moves
    
    def __init__(self):
        self.knight_moves = self._precompute_knight_moves()
        self.king_moves = self._precompute_king_moves()
        # Add direction vectors for sliding pieces
        self.bishop_dirs = [(-1,-1), (-1,1), (1,-1), (1,1)]  # 4 diagonals
        self.rook_dirs = [(-1,0), (1,0), (0,-1), (0,1)]      # 4 straight
        self.queen_dirs = self.bishop_dirs + self.rook_dirs   # All 8
    
    def get_sliding_moves(self, square, board, color, directions):
        """Generic sliding piece move generator. Works for bishop, rook, queen."""
        moves = []
        rank = square // 8
        file = square % 8
        enemy_color = BLACK if color == WHITE else WHITE
        
        for rank_dir, file_dir in directions:
            new_rank, new_file = rank + rank_dir, file + file_dir
            
            # Keep sliding in this direction until blocked
            while 0 <= new_rank < 8 and 0 <= new_file < 8:
                target = new_rank * 8 + new_file
                piece = board.squares[target]
                
                if piece == EMPTY:
                    moves.append(target)  # Empty square, can move here
                elif (piece & 8) == enemy_color:
                    moves.append(target)  # Capture enemy, then stop
                    break
                else:
                    break  # Friendly piece, stop before it
                
                new_rank += rank_dir
                new_file += file_dir
        
        return moves
    
    def get_bishop_moves(self, square, board, color):
        return self.get_sliding_moves(square, board, color, self.bishop_dirs)
    
    def get_rook_moves(self, square, board, color):
        return self.get_sliding_moves(square, board, color, self.rook_dirs)
    
    def get_queen_moves(self, square, board, color):
        return self.get_sliding_moves(square, board, color, self.queen_dirs)
    
    def get_pawn_moves(self, square, board, color):
        """Get pawn moves (without en passant for now)."""
        moves = []
        rank = square // 8
        file = square % 8
        
        # Direction: White pawns move UP (+1), Black pawns move DOWN (-1)
        direction = 1 if color == WHITE else -1
        start_rank = 1 if color == WHITE else 6  # Starting rank for double move
        
        # Forward move (single step)
        forward_square = (rank + direction) * 8 + file
        if 0 <= forward_square < 64 and board.squares[forward_square] == EMPTY:
            moves.append(forward_square)
            
            # Double step from starting position
            if rank == start_rank:
                double_forward = (rank + 2 * direction) * 8 + file
                if board.squares[double_forward] == EMPTY:
                    moves.append(double_forward)
        
        # Diagonal captures
        for file_offset in [-1, 1]:
            capture_file = file + file_offset
            if 0 <= capture_file < 8:
                capture_square = (rank + direction) * 8 + capture_file
                if 0 <= capture_square < 64:
                    target_piece = board.squares[capture_square]
                    enemy_color = BLACK if color == WHITE else WHITE
                    if target_piece != EMPTY and (target_piece & 8) == enemy_color:
                        moves.append(capture_square)
        
        return moves
    
    def get_all_moves(self, board, color):
        """Generate all pseudo-legal moves for a given color."""
        all_moves = []
        
        for square in range(64):
            piece = board.squares[square]
            
            # Skip empty squares and opponent pieces
            if piece == EMPTY or (piece & 8) != color:
                continue
            
            # Get piece type (lower 3 bits)
            piece_type = piece & 7
            
            if piece_type == PAWN:
                moves = self.get_pawn_moves(square, board, color)
            elif piece_type == KNIGHT:
                moves = self.get_knight_moves(square, board, color)
            elif piece_type == BISHOP:
                moves = self.get_bishop_moves(square, board, color)
            elif piece_type == ROOK:
                moves = self.get_rook_moves(square, board, color)
            elif piece_type == QUEEN:
                moves = self.get_queen_moves(square, board, color)
            elif piece_type == KING:
                moves = self.get_king_moves(square, board, color)
            else:
                continue
            
            # Add each move as (from_square, to_square)
            for target in moves:
                all_moves.append((square, target))
        
        return all_moves