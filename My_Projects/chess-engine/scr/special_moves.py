"""
Special chess moves - Castling, En Passant, Pawn Promotion
"""
from constants import EMPTY, WHITE, BLACK, WHITE_KING, BLACK_KING, WHITE_ROOK, BLACK_ROOK, PAWN, KING


def get_castling_moves(board, color, moves_list):
    """Add castling moves if available."""
    king_square = 4 if color == WHITE else 60  # e1 or e8
    king_piece = WHITE_KING if color == WHITE else BLACK_KING
    rook_piece = WHITE_ROOK if color == WHITE else BLACK_ROOK
    
    # Check if king is on starting square and hasn't moved
    if board.squares[king_square] != king_piece:
        return
    
    # Kingside castling
    kingside_rook_sq = 7 if color == WHITE else 63
    kingside_empty = [5, 6] if color == WHITE else [61, 62]
    
    if board.squares[kingside_rook_sq] == rook_piece:
        if all(board.squares[sq] == EMPTY for sq in kingside_empty):
            # Check that king doesn't move through check
            enemy = BLACK if color == WHITE else WHITE
            if not board.is_square_attacked(king_square, enemy) and \
               not board.is_square_attacked(kingside_empty[0], enemy) and \
               not board.is_square_attacked(kingside_empty[1], enemy):
                moves_list.append((king_square, king_square + 2))  # Castling move
    
    # Queenside castling
    queenside_rook_sq = 0 if color == WHITE else 56
    queenside_empty = [3, 2, 1] if color == WHITE else [59, 58, 57]
    
    if board.squares[queenside_rook_sq] == rook_piece:
        if all(board.squares[sq] == EMPTY for sq in queenside_empty):
            enemy = BLACK if color == WHITE else WHITE
            if not board.is_square_attacked(king_square, enemy) and \
               not board.is_square_attacked(queenside_empty[0], enemy) and \
               not board.is_square_attacked(queenside_empty[1], enemy):
                moves_list.append((king_square, king_square - 2))  # Castling move


def get_en_passant_moves(board, color, last_move, moves_list):
    """Add en passant moves if available."""
    if last_move is None:
        return
    
    from_sq, to_sq = last_move
    moved_piece = board.squares[to_sq]
    
    # Check if last move was a pawn double push
    if moved_piece & 7 != PAWN:
        return
    
    # Check if it moved two squares
    if abs(to_sq - from_sq) != 16:
        return
    
    # Get the square between (where en passant capture happens)
    en_passant_square = (from_sq + to_sq) // 2
    
    # Check adjacent pawns of opposite color
    direction = 1 if color == WHITE else -1
    pawn_piece = (PAWN | color)
    
    # Check left and right of the en passant square
    for offset in [-1, 1]:
        pawn_square = en_passant_square + offset
        if 0 <= pawn_square < 64 and board.squares[pawn_square] == pawn_piece:
            # Valid en passant
            capture_square = en_passant_square + (8 if color == WHITE else -8)
            moves_list.append((pawn_square, capture_square))


def handle_promotion(board, to_square):
    """Handle pawn promotion - auto-queen for now."""
    piece = board.squares[to_square]
    piece_type = piece & 7
    piece_color = piece & 8
    
    if piece_type == PAWN:
        rank = to_square // 8
        if rank == 7 or rank == 0:  # Reached last rank
            from constants import QUEEN
            board.squares[to_square] = QUEEN | piece_color  # Promote to queen


def make_move_with_specials(board, from_sq, to_sq):
    """Make a move handling castling, en passant, and promotion."""
    piece = board.squares[from_sq]
    piece_type = piece & 7
    
    # Handle castling - move the rook too
    if piece_type == KING:
        if abs(to_sq - from_sq) == 2:  # Castling
            if to_sq > from_sq:  # Kingside
                rook_from = 7 if from_sq == 4 else 63
                rook_to = 5 if from_sq == 4 else 61
            else:  # Queenside
                rook_from = 0 if from_sq == 4 else 56
                rook_to = 3 if from_sq == 4 else 59
            board.squares[rook_to] = board.squares[rook_from]
            board.squares[rook_from] = EMPTY
    
    # Handle en passant capture
    if piece_type == PAWN:
        if abs(to_sq - from_sq) % 8 != 0 and board.squares[to_sq] == EMPTY:
            # En passant - remove the captured pawn
            captured_pawn_sq = to_sq - 8 if (piece & 8) == WHITE else to_sq + 8
            board.squares[captured_pawn_sq] = EMPTY
    
    # Make the move
    board.squares[to_sq] = piece
    board.squares[from_sq] = EMPTY
    
    # Handle promotion
    handle_promotion(board, to_sq)
    
    # Switch turns
    from constants import WHITE, BLACK
    board.current_player = BLACK if board.current_player == WHITE else WHITE