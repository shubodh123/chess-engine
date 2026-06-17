# from board import Board
# from move_generator import MoveGenerator
# from constants import WHITE

# # def main():
# board = Board()
# # board.display() 
# gen = MoveGenerator()

# # Test knight moves from b1 (square index 1)
# knight_moves = gen.get_knight_moves(1, board, WHITE)
# print(f"Knight on b1 can move to: {knight_moves}")
# # Should show squares 16 (a3) and 18 (c3)

# # if __name__ == "__main__":
# #     main()



# from board import Board
# from move_generator import MoveGenerator
# from constants import WHITE, BLACK

# board = Board()
# gen = MoveGenerator()

# # Test multiple pieces
# print("Knight on b1:", gen.get_knight_moves(1, board, WHITE))
# print("Bishop on c1:", gen.get_bishop_moves(2, board, WHITE))  # Should be empty (blocked)
# print("Pawn on e2:", gen.get_pawn_moves(12, board, WHITE))    # e2 = index 12
# print("Rook on a8:", gen.get_rook_moves(56, board, BLACK))    # Should be empty (blocked)

# from board import Board
# from constants import WHITE, BLACK

# board = Board()

# # Get legal moves for white
# legal_moves = board.get_legal_moves(WHITE)
# print(f"White has {len(legal_moves)} legal moves")
# print("First 5 moves:", legal_moves[:5])

# from board import Board
# from search import get_best_move
# from constants import WHITE, BLACK, PIECE_SYMBOLS
# from special_moves import make_move_with_specials


# def get_human_move(board):
#     """Get a move from the human player."""
#     while True:
#         try:
#             move_str = input("Enter move (e.g., e2e4): ").strip().lower()
#             if len(move_str) != 4:
#                 print("Invalid format. Use like 'e2e4'")
#                 continue
            
#             # Convert algebraic to square indices
#             file_from = ord(move_str[0]) - ord('a')
#             rank_from = int(move_str[1]) - 1
#             file_to = ord(move_str[2]) - ord('a')
#             rank_to = int(move_str[3]) - 1
            
#             from_sq = rank_from * 8 + file_from
#             to_sq = rank_to * 8 + file_to
            
#             legal_moves = board.get_legal_moves(board.current_player)
#             if (from_sq, to_sq) in legal_moves:
#                 return (from_sq, to_sq)
#             else:
#                 print("Illegal move! Try again.")
#         except (ValueError, IndexError):
#             print("Invalid input. Use format: e2e4")


# def main():
#     print("=== Chess Engine ===")
#     print("You play as White. Enter moves like 'e2e4'")
#     print("Engine is thinking at depth 3...\n")
    
#     board = Board()
#     board.display()
    
#     while True:
#         # Human's turn (White)
#         if board.current_player == WHITE:
#             move = get_human_move(board)
#             make_move_with_specials(board, move[0], move[1])
#             board.last_move = move
        
#         # Engine's turn (Black)
#         else:
#             print("\nEngine is thinking...")
#             move = get_best_move(board, depth=3)
#             if move is None:
#                 print("Engine has no legal moves!")
#                 break
#             make_move_with_specials(board, move[0], move[1])
#             board.last_move = move
        
#         board.display()
        
#         # Check game state
#         legal_moves = board.get_legal_moves(board.current_player)
#         if not legal_moves:
#             if board.is_in_check(board.current_player):
#                 winner = "Black" if board.current_player == WHITE else "White"
#                 print(f"Checkmate! {winner} wins!")
#             else:
#                 print("Stalemate! It's a draw!")
#             break


# if __name__ == "__main__":
#     main()

"""
Chess Engine - Main Entry Point with GUI
"""
# from board import Board
# from search import get_best_move
# from gui import ChessGUI
# from coach import ChessCoach
# import os

# # Your API key - paste it here (keep this file private!)
# API_KEY = "AQ.Ab8RN6KZHf-B8GhY1PDtWOM9zFFw3O-ECHNuzoCA60QcAY6r-Q"  # Replace with your actual key



# def main():
#     print("Starting Chess Engine with GUI...")
#     print("Close the window to exit.")
    
#     board = Board()
#     gui = ChessGUI(board, get_best_move)
#     gui = ChessGUI(board, get_best_move, coach)
#     gui.run()


# if __name__ == "__main__":
#     main()


from board import Board
from search import get_best_move
from gui import ChessGUI
from coach import ChessCoach

API_KEY = "AQ.Ab8RN6KZHf-B8GhY1PDtWOM9zFFw3O-ECHNuzoCA60QcAY6r-Q"


def main():
    print("Starting Chess Engine with AI Coach...")
    print("Close the window to exit.")
    
    board = Board()
    coach = ChessCoach(API_KEY)  # ← This line creates coach
    gui = ChessGUI(board, get_best_move, coach)
    gui.run()


if __name__ == "__main__":
    main()