# """
# Chess GUI using Pygame - Enhanced Version
# """
# import pygame
# from constants import EMPTY, WHITE, BLACK, PIECE_SYMBOLS
# from special_moves import make_move_with_specials


# # Board colors for each player's turn
# WHITE_TURN_LIGHT = (240, 217, 181)   # Beige
# WHITE_TURN_DARK = (181, 136, 99)     # Brown
# BLACK_TURN_LIGHT = (169, 189, 208)   # Light blue-gray
# BLACK_TURN_DARK = (97, 127, 148)     # Dark blue-gray

# HIGHLIGHT = (255, 255, 0, 150)       # Yellow highlight for selected piece
# LEGAL_DOT = (0, 0, 0, 100)           # Semi-transparent dot for legal moves
# LEGAL_CAPTURE = (0, 0, 0, 150)       # Darker for capture indicators
# TEXT_COLOR = (255, 255, 255)
# BG_COLOR = (50, 50, 50)
# PANEL_COLOR = (65, 65, 65)


# class ChessGUI:
#     def __init__(self, board, search_func, coach = None):
#         pygame.init()
#         self.board = board
#         self.get_best_move = search_func
#         # self.piece_images = self._load_piece_images()
        
#         self.SQUARE_SIZE = 80
#         self.BOARD_SIZE = self.SQUARE_SIZE * 8
#         self.SIDEBAR = 280
#         self.WINDOW_WIDTH = self.BOARD_SIZE + self.SIDEBAR
#         self.WINDOW_HEIGHT = self.BOARD_SIZE
        
#         self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
#         pygame.display.set_caption("Chess Engine")
        
#         self.piece_font = pygame.font.Font(None, 60)
#         self.small_font = pygame.font.Font(None, 22)
#         self.title_font = pygame.font.Font(None, 28)
#         self.clock = pygame.time.Clock()
        
#         self.selected_square = None
#         self.legal_moves = []  # Stores legal target squares for selected piece
#         self.human_color = WHITE
#         self.engine_thinking = False
#         self.move_history = []
#         self.game_over = False
#         self.result_message = ""

#         self.piece_images = self._load_piece_images()
#         # self.coach = coach
#         # self.coach_analysis = ""
#         self.coach = coach
#         self.coach_analysis = "Press 'C' to activate coach"
#         self.coach_warning = None  # Warning before move

#     def _load_piece_images(self):
#         """Load PNG piece images."""
#         import os
#         pieces = {}
#         piece_names = {
#             WHITE | 6: 'wK',   # King
#             WHITE | 5: 'wQ',   # Queen
#             WHITE | 4: 'wR',   # Rook
#             WHITE | 3: 'wB',   # Bishop
#             WHITE | 2: 'wN',   # Knight
#             WHITE | 1: 'wP',   # Pawn
#             BLACK | 6: 'bK',
#             BLACK | 5: 'bQ',
#             BLACK | 4: 'bR',
#             BLACK | 3: 'bB',
#             BLACK | 2: 'bN',
#             BLACK | 1: 'bP',
#         }
        
#         for piece_code, filename in piece_names.items():
#             path = os.path.join('Pieces', f'{filename}.png')
#             if os.path.exists(path):
#                 image = pygame.image.load(path)
#                 image = pygame.transform.scale(image, (self.SQUARE_SIZE, self.SQUARE_SIZE))
#                 pieces[piece_code] = image
#             else:
#                 print(f"Warning: {path} not found")
        
#         return pieces
    
#     def get_board_colors(self):
#         """Return light and dark square colors based on current player."""
#         if self.board.current_player == WHITE:
#             return WHITE_TURN_LIGHT, WHITE_TURN_DARK
#         else:
#             return BLACK_TURN_LIGHT, BLACK_TURN_DARK
    
#     def draw_board(self):
#         """Draw the chess board squares with turn-based colors."""
#         light_color, dark_color = self.get_board_colors()
        
#         for rank in range(8):
#             for file in range(8):
#                 if (rank + file) % 2 == 0:
#                     color = light_color
#                 else:
#                     color = dark_color
                
#                 x = file * self.SQUARE_SIZE
#                 y = (7 - rank) * self.SQUARE_SIZE
                
#                 pygame.draw.rect(self.screen, color, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))
                
#                 # Draw legal move indicators
#                 square = rank * 8 + file
#                 if square in self.legal_moves:
#                     self.draw_legal_move_indicator(x, y, square)
                
#                 # Highlight selected square
#                 if self.selected_square is not None:
#                     sel_rank = self.selected_square // 8
#                     sel_file = self.selected_square % 8
#                     if rank == sel_rank and file == sel_file:
#                         highlight = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
#                         highlight.fill(HIGHLIGHT)
#                         self.screen.blit(highlight, (x, y))
    
#     def draw_legal_move_indicator(self, x, y, square):
#         """Draw dots for legal moves, circles for captures."""
#         center_x = x + self.SQUARE_SIZE // 2
#         center_y = y + self.SQUARE_SIZE // 2
        
#         if self.board.squares[square] == EMPTY:
#             # Small dot for empty squares
#             dot_radius = 12
#             dot_surface = pygame.Surface((dot_radius * 2, dot_radius * 2), pygame.SRCALPHA)
#             pygame.draw.circle(dot_surface, (0, 0, 0, 100), (dot_radius, dot_radius), dot_radius)
#             self.screen.blit(dot_surface, (center_x - dot_radius, center_y - dot_radius))
#         else:
#             # Thick circle around capturable pieces
#             circle_radius = self.SQUARE_SIZE // 2 - 4
#             pygame.draw.circle(self.screen, (0, 0, 0, 150), (center_x, center_y), circle_radius, 4)
    
#     def draw_pieces(self):
#         """Draw chess pieces using PNG images."""
#         for square in range(64):
#             piece = self.board.squares[square]
#             if piece == EMPTY:
#                 continue
            
#             rank = square // 8
#             file = square % 8
            
#             x = file * self.SQUARE_SIZE
#             y = (7 - rank) * self.SQUARE_SIZE
            
#             if piece in self.piece_images:
#                 self.screen.blit(self.piece_images[piece], (x, y))
#             else:
#                 # Fallback to unicode if image missing
#                 symbol = PIECE_SYMBOLS[piece]
#                 text = self.piece_font.render(symbol, True, (0, 0, 0))
#                 text_rect = text.get_rect(center=(x + self.SQUARE_SIZE//2, y + self.SQUARE_SIZE//2))
#                 self.screen.blit(text, text_rect)

#     def draw_sidebar(self):
#         """Draw the sidebar with game info."""
#         sidebar_rect = pygame.Rect(self.BOARD_SIZE, 0, self.SIDEBAR, self.WINDOW_HEIGHT)
#         pygame.draw.rect(self.screen, BG_COLOR, sidebar_rect)
        
#         y_offset = 20
        
#         # Title
#         title = self.title_font.render("CHESS ENGINE", True, TEXT_COLOR)
#         self.screen.blit(title, (self.BOARD_SIZE + 20, y_offset))
#         y_offset += 40
        
#         # Separator line
#         pygame.draw.line(self.screen, (100, 100, 100), 
#                         (self.BOARD_SIZE + 15, y_offset), 
#                         (self.WINDOW_WIDTH - 15, y_offset), 1)
#         y_offset += 15
        
#         # Turn indicator with colored dot
#         if self.board.current_player == WHITE:
#             turn_text = "WHITE'S TURN"
#             dot_color = (255, 255, 255)
#             turn_color = TEXT_COLOR
#         else:
#             turn_text = "BLACK'S TURN"
#             dot_color = (50, 50, 50)
#             turn_color = (180, 180, 180)
        
#         pygame.draw.circle(self.screen, dot_color, (self.BOARD_SIZE + 25, y_offset + 10), 8)
#         pygame.draw.circle(self.screen, TEXT_COLOR, (self.BOARD_SIZE + 25, y_offset + 10), 8, 1)
        
#         turn = self.small_font.render(turn_text, True, turn_color)
#         self.screen.blit(turn, (self.BOARD_SIZE + 45, y_offset))
#         y_offset += 35
        
#         # Player info panel
#         panel_rect = pygame.Rect(self.BOARD_SIZE + 10, y_offset, self.SIDEBAR - 20, 50)
#         pygame.draw.rect(self.screen, PANEL_COLOR, panel_rect, border_radius=5)
        
#         you_text = self.small_font.render("You: White", True, TEXT_COLOR)
#         engine_text = self.small_font.render("Engine: Black", True, (200, 200, 200))
#         self.screen.blit(you_text, (self.BOARD_SIZE + 20, y_offset + 5))
#         self.screen.blit(engine_text, (self.BOARD_SIZE + 20, y_offset + 28))
#         y_offset += 60
        
#         # Separator
#         pygame.draw.line(self.screen, (100, 100, 100), 
#                         (self.BOARD_SIZE + 15, y_offset), 
#                         (self.WINDOW_WIDTH - 15, y_offset), 1)
#         y_offset += 15
        
#         # Move history
#         history_title = self.small_font.render("MOVE HISTORY", True, TEXT_COLOR)
#         self.screen.blit(history_title, (self.BOARD_SIZE + 20, y_offset))
#         y_offset += 25
        
#         # Show moves (alternating colors for readability)
#         start_idx = max(0, len(self.move_history) - 14)
#         for i in range(start_idx, len(self.move_history)):
#             move_num = i + 1
#             if move_num % 2 == 1:
#                 move_color = (220, 220, 220)
#             else:
#                 move_color = (160, 160, 160)
            
#             move_text = f"{move_num:2d}. {self.move_history[i]}"
#             move_render = self.small_font.render(move_text, True, move_color)
#             self.screen.blit(move_render, (self.BOARD_SIZE + 20, y_offset))
#             y_offset += 22
        
#         # Bottom section
#         if self.engine_thinking:
#             y_offset = self.WINDOW_HEIGHT - 70
#             think_bg = pygame.Rect(self.BOARD_SIZE + 10, y_offset - 5, self.SIDEBAR - 20, 55)
#             pygame.draw.rect(self.screen, (80, 80, 30), think_bg, border_radius=5)
            
#             thinking_text = self.small_font.render("ENGINE THINKING...", True, (255, 255, 0))
#             self.screen.blit(thinking_text, (self.BOARD_SIZE + 20, y_offset))
        
#         if self.game_over:
#             y_offset = self.WINDOW_HEIGHT - 45
#             result_bg = pygame.Rect(self.BOARD_SIZE, y_offset - 5, self.SIDEBAR, 50)
#             pygame.draw.rect(self.screen, (100, 20, 20), result_bg)
            
#             result = self.small_font.render(self.result_message, True, (255, 200, 200))
#             result_rect = result.get_rect(center=(self.BOARD_SIZE + self.SIDEBAR // 2, y_offset + 15))
#             self.screen.blit(result, result_rect)
#             self.draw_coach_panel()
    

#     # def draw_coach_panel(self):
#     #     """Draw AI coach analysis panel."""
#     #     if not self.coach:
#     #         return
        
#     #     y_offset = self.WINDOW_HEIGHT - 190
        
#     #     # Panel background
#     #     coach_rect = pygame.Rect(self.BOARD_SIZE + 5, y_offset, self.SIDEBAR - 10, 160)
#     #     pygame.draw.rect(self.screen, (25, 35, 55), coach_rect, border_radius=8)
#     #     pygame.draw.rect(self.screen, (80, 150, 220), coach_rect, 2, border_radius=8)
        
#     #     # Title
#     #     title = self.small_font.render("AI COACH (Gemini):", True, (80, 180, 255))
#     #     self.screen.blit(title, (self.BOARD_SIZE + 15, y_offset + 8))
        
#     #     if self.coach_analysis:
#     #         # Word-wrap analysis text
#     #         words = self.coach_analysis.split()
#     #         lines = []
#     #         current = ""
#     #         for word in words:
#     #             test = current + " " + word if current else word
#     #             if self.small_font.size(test)[0] < self.SIDEBAR - 30:
#     #                 current = test
#     #             else:
#     #                 lines.append(current)
#     #                 current = word
#     #         if current:
#     #             lines.append(current)
            
#     #         for i, line in enumerate(lines[:7]):
#     #             text = self.small_font.render(line, True, (210, 210, 210))
#     #             self.screen.blit(text, (self.BOARD_SIZE + 15, y_offset + 30 + i * 20))
#     #     else:
#     #         # Waiting message before any moves
#     #         msg = self.small_font.render("Make a move to get", True, (150, 150, 150))
#     #         msg2 = self.small_font.render("coach feedback!", True, (150, 150, 150))
#     #         self.screen.blit(msg, (self.BOARD_SIZE + 15, y_offset + 40))
#     #         self.screen.blit(msg2, (self.BOARD_SIZE + 15, y_offset + 62))
#     def draw_coach_panel(self):
#         """Draw AI coach panel in sidebar."""
#         if not self.coach:
#             return
        
#         y_offset = self.WINDOW_HEIGHT - 200
        
#         # Panel background (different colors for active/inactive)
#         if self.coach.active:
#             bg = (20, 40, 30)  # Green-ish when active
#             border = (80, 200, 120)
#             status = "ACTIVE"
#         else:
#             bg = (40, 40, 45)
#             border = (100, 100, 100)
#             status = "OFF (Press C)"
        
#         coach_rect = pygame.Rect(self.BOARD_SIZE + 5, y_offset, self.SIDEBAR - 10, 170)
#         pygame.draw.rect(self.screen, bg, coach_rect, border_radius=8)
#         pygame.draw.rect(self.screen, border, coach_rect, 2, border_radius=8)
        
#         # Title with status
#         title = self.small_font.render(f"AI COACH [{status}]", True, border)
#         self.screen.blit(title, (self.BOARD_SIZE + 15, y_offset + 8))
        
#         # Mode indicator
#         mode_text = f"Mode: {self.coach.mode.upper()}"
#         mode = self.small_font.render(mode_text, True, (180, 180, 180))
#         self.screen.blit(mode, (self.BOARD_SIZE + 15, y_offset + 30))
        
#         # Warning (if any)
#         if self.coach_warning and "WARNING" in self.coach_warning:
#             warn_text = self.small_font.render(self.coach_warning[:50], True, (255, 100, 100))
#             self.screen.blit(warn_text, (self.BOARD_SIZE + 15, y_offset + 52))
        
#         # Main analysis text
#         if self.coach_analysis:
#             words = self.coach_analysis.split()
#             lines = []
#             current = ""
#             for word in words:
#                 test = current + " " + word if current else word
#                 if self.small_font.size(test)[0] < self.SIDEBAR - 30:
#                     current = test
#                 else:
#                     lines.append(current)
#                     current = word
#             if current:
#                 lines.append(current)
            
#             start_y = y_offset + 75
#             for i, line in enumerate(lines[:5]):
#                 text = self.small_font.render(line, True, (210, 210, 210))
#                 self.screen.blit(text, (self.BOARD_SIZE + 15, start_y + i * 20))
    
#     def get_square_from_click(self, x, y):
#         """Convert mouse coordinates to board square."""
#         if x >= self.BOARD_SIZE:
#             return None
        
#         file = x // self.SQUARE_SIZE
#         rank = 7 - (y // self.SQUARE_SIZE)
#         return rank * 8 + file
    
#     def get_algebraic(self, move):
#         """Convert move to simple algebraic notation."""
#         from_sq, to_sq = move
#         files = 'abcdefgh'
        
#         from_file = files[from_sq % 8]
#         from_rank = str(from_sq // 8 + 1)
#         to_file = files[to_sq % 8]
#         to_rank = str(to_sq // 8 + 1)
        
#         return f"{from_file}{from_rank}{to_file}{to_rank}"
    
#     # def handle_click(self, square):
#     #     """Handle mouse click on a square."""
#     #     # Coach warning before move
#     #     if self.coach and self.coach.active:
#     #         move = (self.selected_square, square)
#     #         self.coach_warning = self.coach.warn_before_move(self.board, move)
#     #         if self.coach_warning:
#     #             self.coach_analysis = self.coach_warning
        
#     #     move = (self.selected_square, square)
#     #     make_move_with_specials(...)

#     #     if self.game_over or self.engine_thinking:
#     #         return
        
#     #     if self.selected_square is None:
#     #         # Select a piece and show its legal moves
#     #         piece = self.board.squares[square]
#     #         if piece != EMPTY and (piece & 8) == self.human_color:
#     #             self.selected_square = square
#     #             # Calculate legal destinations for this piece only
#     #             all_legal = self.board.get_legal_moves(self.human_color)
#     #             self.legal_moves = [move[1] for move in all_legal if move[0] == square]
#     #     else:
#     #         # Try to make a move
#     #         if square in self.legal_moves:
#     #             move = (self.selected_square, square)
#     #             make_move_with_specials(self.board, move[0], move[1])
#     #             self.board.last_move = move
#     #             self.move_history.append(self.get_algebraic(move))
#     #             self.selected_square = None
#     #             self.legal_moves = []
                
#     #             # Get coach analysis of human move
#     #             if self.coach:
#     #                 try:
#     #                     self.coach_analysis = self.coach.explain_move(self.board, move)
#     #                 except:
#     #                     self.coach_analysis = "Coach analyzing your move..."
                
#     #             self.check_game_state()
                
#     #             # Let engine respond
#     #             if not self.game_over:
#     #                 self.engine_thinking = True
#     #                 self.draw_all()
#     #                 pygame.display.flip()
                    
#     #                 engine_move = self.get_best_move(self.board, depth=3)
#     #                 if engine_move:
#     #                     make_move_with_specials(self.board, engine_move[0], engine_move[1])
#     #                     self.board.last_move = engine_move
#     #                     self.move_history.append(self.get_algebraic(engine_move))
                        
#     #                     # Get coach analysis of engine move
#     #                     if self.coach:
#     #                         try:
#     #                             self.coach_analysis = self.coach.analyze_position(self.board, engine_move)
#     #                         except:
#     #                             self.coach_analysis = "Coach analyzing position..."
                    
#     #                 self.engine_thinking = False
#     #                 self.check_game_state()
#     #         else:
#     #             # Clicked elsewhere - deselect or switch piece
#     #             piece = self.board.squares[square]
#     #             if piece != EMPTY and (piece & 8) == self.human_color:
#     #                 self.selected_square = square
#     #                 all_legal = self.board.get_legal_moves(self.human_color)
#     #                 self.legal_moves = [move[1] for move in all_legal if move[0] == square]
#     #             else:
#     #                 self.selected_square = None
#     #                 self.legal_moves = []

#     #     if self.coach and self.coach.active:
#     #                 self.coach_analysis = self.coach.analyze_move(self.board, move)
#     #                 self.coach_warning = None


#     def handle_click(self, square):
#         """Handle mouse click on a square."""
#         if self.game_over or self.engine_thinking:
#             return
        
#         if self.selected_square is None:
#             # Select a piece and show its legal moves
#             piece = self.board.squares[square]
#             if piece != EMPTY and (piece & 8) == self.human_color:
#                 self.selected_square = square
#                 all_legal = self.board.get_legal_moves(self.human_color)
#                 self.legal_moves = [move[1] for move in all_legal if move[0] == square]
#         else:
#             # Try to make a move
#             if square in self.legal_moves:
#                 move = (self.selected_square, square)
                
#                 # Coach warning BEFORE move (if coach is active)
#                 if self.coach and self.coach.active:
#                     self.coach_warning = self.coach.warn_before_move(self.board, move)
#                     if self.coach_warning:
#                         self.coach_analysis = self.coach_warning
                
#                 make_move_with_specials(self.board, move[0], move[1])
#                 self.board.last_move = move
#                 self.move_history.append(self.get_algebraic(move))
#                 self.selected_square = None
#                 self.legal_moves = []
                
#                 # Coach analysis AFTER human move
#                 if self.coach and self.coach.active:
#                     self.coach_analysis = self.coach.analyze_move(self.board, move)
#                     self.coach_warning = None
                
#                 self.check_game_state()
                
#                 # Let engine respond
#                 if not self.game_over:
#                     self.engine_thinking = True
#                     self.draw_all()
#                     pygame.display.flip()
                    
#                     engine_move = self.get_best_move(self.board, depth=3)
#                     if engine_move:
#                         make_move_with_specials(self.board, engine_move[0], engine_move[1])
#                         self.board.last_move = engine_move
#                         self.move_history.append(self.get_algebraic(engine_move))
                        
#                         # Coach hint AFTER engine move
#                         if self.coach and self.coach.active:
#                             hint = self.coach.get_hint(self.board)
#                             self.coach_analysis = hint
                    
#                     self.engine_thinking = False
#                     self.check_game_state()
#             else:
#                 # Clicked elsewhere - deselect or switch piece
#                 piece = self.board.squares[square]
#                 if piece != EMPTY and (piece & 8) == self.human_color:
#                     self.selected_square = square
#                     all_legal = self.board.get_legal_moves(self.human_color)
#                     self.legal_moves = [move[1] for move in all_legal if move[0] == square]
#                 else:
#                     self.selected_square = None
#                     self.legal_moves = []

#     # def draw_coach_panel(self):
#     #     """Draw AI coach analysis panel."""
#     #     if not self.coach or not self.coach_analysis:
#     #         return
        
#     #     y_offset = self.WINDOW_HEIGHT - 190
        
#     #     # Panel background
#     #     coach_rect = pygame.Rect(self.BOARD_SIZE + 5, y_offset, self.SIDEBAR - 10, 160)
#     #     pygame.draw.rect(self.screen, (25, 35, 55), coach_rect, border_radius=8)
#     #     pygame.draw.rect(self.screen, (80, 150, 220), coach_rect, 2, border_radius=8)
        
#     #     # Title
#     #     title = self.small_font.render("AI COACH:", True, (80, 180, 255))
#     #     self.screen.blit(title, (self.BOARD_SIZE + 15, y_offset + 8))
        
#     #     # Word-wrap analysis text
#     #     words = self.coach_analysis.split()
#     #     lines = []
#     #     current = ""
#     #     for word in words:
#     #         test = current + " " + word if current else word
#     #         if self.small_font.size(test)[0] < self.SIDEBAR - 30:
#     #             current = test
#     #         else:
#     #             lines.append(current)
#     #             current = word
#     #     if current:
#     #         lines.append(current)
        
#     #     for i, line in enumerate(lines[:7]):
#     #         text = self.small_font.render(line, True, (210, 210, 210))
#     #         self.screen.blit(text, (self.BOARD_SIZE + 15, y_offset + 30 + i * 20))
    
#     # def check_game_state(self):
#     #     """Check for checkmate/stalemate."""
#     #     legal_moves = self.board.get_legal_moves(self.board.current_player)
#     #     if not legal_moves:
#     #         self.game_over = True
#     #         if self.board.is_in_check(self.board.current_player):
#     #             winner = "Black" if self.board.current_player == WHITE else "White"
#     #             self.result_message = f"Checkmate! {winner} wins!"
#     #         else:
#     #             self.result_message = "Stalemate! Draw!"
    
#     def check_game_state(self):
#         """Check for checkmate/stalemate."""
#         legal_moves = self.board.get_legal_moves(self.board.current_player)
#         if not legal_moves:
#             self.game_over = True
#             if self.board.is_in_check(self.board.current_player):
#                 winner = "Black" if self.board.current_player == WHITE else "White"
#                 self.result_message = f"Checkmate! {winner} wins!"
#             else:
#                 self.result_message = "Stalemate! Draw!"
            
#             # Get post-game analysis
#             if self.coach and self.coach.active:
#                 self.coach_analysis = self.coach.post_game_review(
#                     self.move_history, self.result_message
#                 )
    
#     def draw_all(self):
#         """Draw everything."""
#         self.draw_board()
#         self.draw_pieces()
#         self.draw_sidebar()
    
#     # def run(self):
#     #     """Main game loop."""
#     #     running = True
        
#     #     while running:
#     #         for event in pygame.event.get():
#     #             if event.type == pygame.QUIT:
#     #                 running = False
                
#     #             elif event.type == pygame.MOUSEBUTTONDOWN:
#     #                 x, y = pygame.mouse.get_pos()
#     #                 square = self.get_square_from_click(x, y)
#     #                 if square is not None:
#     #                     self.handle_click(square)
                
#     #             elif event.type == pygame.KEYDOWN:
#     #                 if event.key == pygame.K_r and self.game_over:
#     #                     # Restart game
#     #                     from board import Board
#     #                     self.__init__(Board(), self.get_best_move)
            
#     #         self.draw_all()
#     #         pygame.display.flip()
#     #         self.clock.tick(60)
#     def run(self):
#         """Main game loop."""
#         running = True
        
#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
                
#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     x, y = pygame.mouse.get_pos()
#                     square = self.get_square_from_click(x, y)
#                     if square is not None:
#                         self.handle_click(square)
                
#                 elif event.type == pygame.KEYDOWN:
#                     # Toggle coach ON/OFF with 'C' key
#                     if event.key == pygame.K_c and self.coach:
#                         status = self.coach.toggle()
#                         if status == "on":
#                             self.coach_analysis = "Coach activated! Make a move."
#                         else:
#                             self.coach_analysis = ""
                    
#                     # Restart game with 'R' key
#                     elif event.key == pygame.K_r and self.game_over:
#                         from board import Board
#                         # Show post-game review if coach is active
#                         if self.coach and self.coach.active:
#                             review = self.coach.post_game_review(self.move_history, self.result_message)
#                             self.coach_analysis = review
#                             self.draw_all()
#                             pygame.display.flip()
#                             pygame.time.wait(5000)  # Show review for 5 seconds
#                         self.__init__(Board(), self.get_best_move, self.coach)
            
#             self.draw_all()
#             pygame.display.flip()
#             self.clock.tick(60)
        
#         pygame.quit()    
#         # pygame.quit()


"""
Chess GUI using Pygame - Enhanced Version
"""
import pygame
from constants import EMPTY, WHITE, BLACK, PIECE_SYMBOLS
from special_moves import make_move_with_specials


# Board colors for each player's turn
WHITE_TURN_LIGHT = (240, 217, 181)   # Beige
WHITE_TURN_DARK = (181, 136, 99)     # Brown
BLACK_TURN_LIGHT = (169, 189, 208)   # Light blue-gray
BLACK_TURN_DARK = (97, 127, 148)     # Dark blue-gray

HIGHLIGHT = (255, 255, 0, 150)       # Yellow highlight for selected piece
LEGAL_DOT = (0, 0, 0, 100)           # Semi-transparent dot for legal moves
LEGAL_CAPTURE = (0, 0, 0, 150)       # Darker for capture indicators
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (50, 50, 50)
PANEL_COLOR = (65, 65, 65)


class ChessGUI:
    def __init__(self, board, search_func, coach = None):
        pygame.init()
        self.board = board
        self.get_best_move = search_func
        # self.piece_images = self._load_piece_images()
        
        self.SQUARE_SIZE = 80
        self.BOARD_SIZE = self.SQUARE_SIZE * 8
        self.SIDEBAR = 280
        self.WINDOW_WIDTH = self.BOARD_SIZE + self.SIDEBAR
        self.WINDOW_HEIGHT = self.BOARD_SIZE
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Chess Engine")
        
        self.piece_font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 28)
        self.clock = pygame.time.Clock()
        
        self.selected_square = None
        self.legal_moves = []  # Stores legal target squares for selected piece
        self.human_color = WHITE
        self.engine_thinking = False
        self.move_history = []
        self.game_over = False
        self.result_message = ""

        self.piece_images = self._load_piece_images()
        # self.coach = coach
        # self.coach_analysis = ""
        self.coach = coach
        self.coach_analysis = "Press 'C' to toggle ON/OFF"
        self.coach_warning = None  # Warning before move
        self.display_player = WHITE  # Tracks color for board visuals (only flips after full round)

    def _load_piece_images(self):
        """Load PNG piece images."""
        import os
        pieces = {}
        piece_names = {
            WHITE | 6: 'wK',   # King
            WHITE | 5: 'wQ',   # Queen
            WHITE | 4: 'wR',   # Rook
            WHITE | 3: 'wB',   # Bishop
            WHITE | 2: 'wN',   # Knight
            WHITE | 1: 'wP',   # Pawn
            BLACK | 6: 'bK',
            BLACK | 5: 'bQ',
            BLACK | 4: 'bR',
            BLACK | 3: 'bB',
            BLACK | 2: 'bN',
            BLACK | 1: 'bP',
        }
        
        for piece_code, filename in piece_names.items():
            path = os.path.join('Pieces', f'{filename}.png')
            if os.path.exists(path):
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (self.SQUARE_SIZE, self.SQUARE_SIZE))
                pieces[piece_code] = image
            else:
                print(f"Warning: {path} not found")
        
        return pieces
    
    def get_board_colors(self):
        """Return light and dark square colors based on display player (human's turn only)."""
        if self.display_player == WHITE:
            return WHITE_TURN_LIGHT, WHITE_TURN_DARK
        else:
            return BLACK_TURN_LIGHT, BLACK_TURN_DARK
    
    def draw_board(self):
        """Draw the chess board squares with turn-based colors."""
        light_color, dark_color = self.get_board_colors()
        
        for rank in range(8):
            for file in range(8):
                if (rank + file) % 2 == 0:
                    color = light_color
                else:
                    color = dark_color
                
                x = file * self.SQUARE_SIZE
                y = (7 - rank) * self.SQUARE_SIZE
                
                pygame.draw.rect(self.screen, color, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))
                
                # Draw legal move indicators
                square = rank * 8 + file
                if square in self.legal_moves:
                    self.draw_legal_move_indicator(x, y, square)
                
                # Highlight selected square
                if self.selected_square is not None:
                    sel_rank = self.selected_square // 8
                    sel_file = self.selected_square % 8
                    if rank == sel_rank and file == sel_file:
                        highlight = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
                        highlight.fill(HIGHLIGHT)
                        self.screen.blit(highlight, (x, y))
    
    def draw_legal_move_indicator(self, x, y, square):
        """Draw dots for legal moves, circles for captures."""
        center_x = x + self.SQUARE_SIZE // 2
        center_y = y + self.SQUARE_SIZE // 2
        
        if self.board.squares[square] == EMPTY:
            # Small dot for empty squares
            dot_radius = 12
            dot_surface = pygame.Surface((dot_radius * 2, dot_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(dot_surface, (0, 0, 0, 100), (dot_radius, dot_radius), dot_radius)
            self.screen.blit(dot_surface, (center_x - dot_radius, center_y - dot_radius))
        else:
            # Thick circle around capturable pieces
            circle_radius = self.SQUARE_SIZE // 2 - 4
            pygame.draw.circle(self.screen, (0, 0, 0, 150), (center_x, center_y), circle_radius, 4)
    
    def draw_pieces(self):
        """Draw chess pieces using PNG images."""
        for square in range(64):
            piece = self.board.squares[square]
            if piece == EMPTY:
                continue
            
            rank = square // 8
            file = square % 8
            
            x = file * self.SQUARE_SIZE
            y = (7 - rank) * self.SQUARE_SIZE
            
            if piece in self.piece_images:
                self.screen.blit(self.piece_images[piece], (x, y))
            else:
                # Fallback to unicode if image missing
                symbol = PIECE_SYMBOLS[piece]
                text = self.piece_font.render(symbol, True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + self.SQUARE_SIZE//2, y + self.SQUARE_SIZE//2))
                self.screen.blit(text, text_rect)

    def draw_sidebar(self):
        """Draw the sidebar with game info."""
        sidebar_rect = pygame.Rect(self.BOARD_SIZE, 0, self.SIDEBAR, self.WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, BG_COLOR, sidebar_rect)
        
        y_offset = 20
        
        # Title
        title = self.title_font.render("CHESS ENGINE", True, TEXT_COLOR)
        self.screen.blit(title, (self.BOARD_SIZE + 20, y_offset))
        y_offset += 40
        
        # Separator line
        pygame.draw.line(self.screen, (100, 100, 100), 
                        (self.BOARD_SIZE + 15, y_offset), 
                        (self.WINDOW_WIDTH - 15, y_offset), 1)
        y_offset += 15
        
        # Turn indicator with colored dot
        if self.board.current_player == WHITE:
            turn_text = "WHITE'S TURN"
            dot_color = (255, 255, 255)
            turn_color = TEXT_COLOR
        else:
            turn_text = "BLACK'S TURN"
            dot_color = (50, 50, 50)
            turn_color = (180, 180, 180)
        
        pygame.draw.circle(self.screen, dot_color, (self.BOARD_SIZE + 25, y_offset + 10), 8)
        pygame.draw.circle(self.screen, TEXT_COLOR, (self.BOARD_SIZE + 25, y_offset + 10), 8, 1)
        
        turn = self.small_font.render(turn_text, True, turn_color)
        self.screen.blit(turn, (self.BOARD_SIZE + 45, y_offset))
        y_offset += 35
        
        # Player info panel
        panel_rect = pygame.Rect(self.BOARD_SIZE + 10, y_offset, self.SIDEBAR - 20, 50)
        pygame.draw.rect(self.screen, PANEL_COLOR, panel_rect, border_radius=5)
        
        you_text = self.small_font.render("You: White", True, TEXT_COLOR)
        engine_text = self.small_font.render("Engine: Black", True, (200, 200, 200))
        self.screen.blit(you_text, (self.BOARD_SIZE + 20, y_offset + 5))
        self.screen.blit(engine_text, (self.BOARD_SIZE + 20, y_offset + 28))
        y_offset += 60
        
        # Separator
        pygame.draw.line(self.screen, (100, 100, 100), 
                        (self.BOARD_SIZE + 15, y_offset), 
                        (self.WINDOW_WIDTH - 15, y_offset), 1)
        y_offset += 15
        
        # Move history
        history_title = self.small_font.render("MOVE HISTORY", True, TEXT_COLOR)
        self.screen.blit(history_title, (self.BOARD_SIZE + 20, y_offset))
        y_offset += 25
        
        # Show moves (alternating colors for readability)
        start_idx = max(0, len(self.move_history) - 14)
        for i in range(start_idx, len(self.move_history)):
            move_num = i + 1
            if move_num % 2 == 1:
                move_color = (220, 220, 220)
            else:
                move_color = (160, 160, 160)
            
            move_text = f"{move_num:2d}. {self.move_history[i]}"
            move_render = self.small_font.render(move_text, True, move_color)
            self.screen.blit(move_render, (self.BOARD_SIZE + 20, y_offset))
            y_offset += 22
        
        # Bottom section
        if self.engine_thinking:
            y_offset = self.WINDOW_HEIGHT - 70
            think_bg = pygame.Rect(self.BOARD_SIZE + 10, y_offset - 5, self.SIDEBAR - 20, 55)
            pygame.draw.rect(self.screen, (80, 80, 30), think_bg, border_radius=5)
            
            thinking_text = self.small_font.render("ENGINE THINKING...", True, (255, 255, 0))
            self.screen.blit(thinking_text, (self.BOARD_SIZE + 20, y_offset))
        
        # Draw coach panel always (not just on game over)
        self.draw_coach_panel()

        if self.game_over:
            y_offset = self.WINDOW_HEIGHT - 45
            result_bg = pygame.Rect(self.BOARD_SIZE, y_offset - 5, self.SIDEBAR, 50)
            pygame.draw.rect(self.screen, (100, 20, 20), result_bg)
            
            result = self.small_font.render(self.result_message, True, (255, 200, 200))
            result_rect = result.get_rect(center=(self.BOARD_SIZE + self.SIDEBAR // 2, y_offset + 15))
            self.screen.blit(result, result_rect)
    

    # def draw_coach_panel(self):
    #     """Draw AI coach analysis panel."""
    #     if not self.coach:
    #         return
        
    #     y_offset = self.WINDOW_HEIGHT - 190
        
    #     # Panel background
    #     coach_rect = pygame.Rect(self.BOARD_SIZE + 5, y_offset, self.SIDEBAR - 10, 160)
    #     pygame.draw.rect(self.screen, (25, 35, 55), coach_rect, border_radius=8)
    #     pygame.draw.rect(self.screen, (80, 150, 220), coach_rect, 2, border_radius=8)
        
    #     # Title
    #     title = self.small_font.render("AI COACH (Gemini):", True, (80, 180, 255))
    #     self.screen.blit(title, (self.BOARD_SIZE + 15, y_offset + 8))
        
    #     if self.coach_analysis:
    #         # Word-wrap analysis text
    #         words = self.coach_analysis.split()
    #         lines = []
    #         current = ""
    #         for word in words:
    #             test = current + " " + word if current else word
    #             if self.small_font.size(test)[0] < self.SIDEBAR - 30:
    #                 current = test
    #             else:
    #                 lines.append(current)
    #                 current = word
    #         if current:
    #             lines.append(current)
            
    #         for i, line in enumerate(lines[:7]):
    #             text = self.small_font.render(line, True, (210, 210, 210))
    #             self.screen.blit(text, (self.BOARD_SIZE + 15, y_offset + 30 + i * 20))
    #     else:
    #         # Waiting message before any moves
    #         msg = self.small_font.render("Make a move to get", True, (150, 150, 150))
    #         msg2 = self.small_font.render("coach feedback!", True, (150, 150, 150))
    #         self.screen.blit(msg, (self.BOARD_SIZE + 15, y_offset + 40))
    #         self.screen.blit(msg2, (self.BOARD_SIZE + 15, y_offset + 62))
    def draw_coach_panel(self):
        """Draw AI coach panel in sidebar."""
        if not self.coach:
            return
        
        y_offset = self.WINDOW_HEIGHT - 200
        
        # Panel background (different colors for active/inactive)
        if self.coach.active:
            bg = (20, 40, 30)  # Green-ish when active
            border = (80, 200, 120)
            status = "ACTIVE"
        else:
            bg = (40, 40, 45)
            border = (100, 100, 100)
            status = "OFF (Press C)"
        
        coach_rect = pygame.Rect(self.BOARD_SIZE + 5, y_offset, self.SIDEBAR - 10, 170)
        pygame.draw.rect(self.screen, bg, coach_rect, border_radius=8)
        pygame.draw.rect(self.screen, border, coach_rect, 2, border_radius=8)
        
        # Title with status
        title = self.small_font.render(f"AI COACH [{status}]", True, border)
        self.screen.blit(title, (self.BOARD_SIZE + 15, y_offset + 8))
        
        # Mode indicator
        mode_text = f"Mode: {self.coach.mode.upper()}"
        mode = self.small_font.render(mode_text, True, (180, 180, 180))
        self.screen.blit(mode, (self.BOARD_SIZE + 15, y_offset + 30))
        
        # Warning (if any)
        if self.coach_warning and "WARNING" in self.coach_warning:
            warn_text = self.small_font.render(self.coach_warning[:50], True, (255, 100, 100))
            self.screen.blit(warn_text, (self.BOARD_SIZE + 15, y_offset + 52))
        
        # Main analysis text
        if self.coach_analysis:
            words = self.coach_analysis.split()
            lines = []
            current = ""
            for word in words:
                test = current + " " + word if current else word
                if self.small_font.size(test)[0] < self.SIDEBAR - 30:
                    current = test
                else:
                    lines.append(current)
                    current = word
            if current:
                lines.append(current)
            
            start_y = y_offset + 75
            for i, line in enumerate(lines[:5]):
                text = self.small_font.render(line, True, (210, 210, 210))
                self.screen.blit(text, (self.BOARD_SIZE + 15, start_y + i * 20))
    
    def get_square_from_click(self, x, y):
        """Convert mouse coordinates to board square."""
        if x >= self.BOARD_SIZE:
            return None
        
        file = x // self.SQUARE_SIZE
        rank = 7 - (y // self.SQUARE_SIZE)
        return rank * 8 + file
    
    def get_algebraic(self, move):
        """Convert move to simple algebraic notation."""
        from_sq, to_sq = move
        files = 'abcdefgh'
        
        from_file = files[from_sq % 8]
        from_rank = str(from_sq // 8 + 1)
        to_file = files[to_sq % 8]
        to_rank = str(to_sq // 8 + 1)
        
        return f"{from_file}{from_rank}{to_file}{to_rank}"
    
    # def handle_click(self, square):
    #     """Handle mouse click on a square."""
    #     # Coach warning before move
    #     if self.coach and self.coach.active:
    #         move = (self.selected_square, square)
    #         self.coach_warning = self.coach.warn_before_move(self.board, move)
    #         if self.coach_warning:
    #             self.coach_analysis = self.coach_warning
        
    #     move = (self.selected_square, square)
    #     make_move_with_specials(...)

    #     if self.game_over or self.engine_thinking:
    #         return
        
    #     if self.selected_square is None:
    #         # Select a piece and show its legal moves
    #         piece = self.board.squares[square]
    #         if piece != EMPTY and (piece & 8) == self.human_color:
    #             self.selected_square = square
    #             # Calculate legal destinations for this piece only
    #             all_legal = self.board.get_legal_moves(self.human_color)
    #             self.legal_moves = [move[1] for move in all_legal if move[0] == square]
    #     else:
    #         # Try to make a move
    #         if square in self.legal_moves:
    #             move = (self.selected_square, square)
    #             make_move_with_specials(self.board, move[0], move[1])
    #             self.board.last_move = move
    #             self.move_history.append(self.get_algebraic(move))
    #             self.selected_square = None
    #             self.legal_moves = []
                
    #             # Get coach analysis of human move
    #             if self.coach:
    #                 try:
    #                     self.coach_analysis = self.coach.explain_move(self.board, move)
    #                 except:
    #                     self.coach_analysis = "Coach analyzing your move..."
                
    #             self.check_game_state()
                
    #             # Let engine respond
    #             if not self.game_over:
    #                 self.engine_thinking = True
    #                 self.draw_all()
    #                 pygame.display.flip()
                    
    #                 engine_move = self.get_best_move(self.board, depth=3)
    #                 if engine_move:
    #                     make_move_with_specials(self.board, engine_move[0], engine_move[1])
    #                     self.board.last_move = engine_move
    #                     self.move_history.append(self.get_algebraic(engine_move))
                        
    #                     # Get coach analysis of engine move
    #                     if self.coach:
    #                         try:
    #                             self.coach_analysis = self.coach.analyze_position(self.board, engine_move)
    #                         except:
    #                             self.coach_analysis = "Coach analyzing position..."
                    
    #                 self.engine_thinking = False
    #                 self.check_game_state()
    #         else:
    #             # Clicked elsewhere - deselect or switch piece
    #             piece = self.board.squares[square]
    #             if piece != EMPTY and (piece & 8) == self.human_color:
    #                 self.selected_square = square
    #                 all_legal = self.board.get_legal_moves(self.human_color)
    #                 self.legal_moves = [move[1] for move in all_legal if move[0] == square]
    #             else:
    #                 self.selected_square = None
    #                 self.legal_moves = []

    #     if self.coach and self.coach.active:
    #                 self.coach_analysis = self.coach.analyze_move(self.board, move)
    #                 self.coach_warning = None


    def handle_click(self, square):
        """Handle mouse click on a square."""
        if self.game_over or self.engine_thinking:
            return
        
        if self.selected_square is None:
            # Select a piece and show its legal moves
            piece = self.board.squares[square]
            if piece != EMPTY and (piece & 8) == self.human_color:
                self.selected_square = square
                all_legal = self.board.get_legal_moves(self.human_color)
                self.legal_moves = [move[1] for move in all_legal if move[0] == square]
        else:
            # Try to make a move
            if square in self.legal_moves:
                move = (self.selected_square, square)
                
                # Coach warning BEFORE move (if coach is active)
                if self.coach and self.coach.active:
                    self.coach_warning = self.coach.warn_before_move(self.board, move)
                    if self.coach_warning:
                        self.coach_analysis = self.coach_warning
                
                make_move_with_specials(self.board, move[0], move[1])
                self.board.last_move = move
                self.move_history.append(self.get_algebraic(move))
                self.selected_square = None
                self.legal_moves = []
                
                # Coach analysis AFTER human move
                if self.coach and self.coach.active:
                    self.coach_analysis = self.coach.analyze_move(self.board, move)
                    self.coach_warning = None
                
                self.check_game_state()
                
                # Let engine respond
                if not self.game_over:
                    self.engine_thinking = True
                    self.draw_all()
                    pygame.display.flip()
                    
                    engine_move = self.get_best_move(self.board, depth=3)
                    if engine_move:
                        make_move_with_specials(self.board, engine_move[0], engine_move[1])
                        self.board.last_move = engine_move
                        self.move_history.append(self.get_algebraic(engine_move))
                        
                        # Coach hint AFTER engine move
                        if self.coach and self.coach.active:
                            hint = self.coach.get_hint(self.board)
                            self.coach_analysis = hint
                    
                    self.engine_thinking = False
                    # Only update visual color after full round (human + engine)
                    self.display_player = WHITE
                    self.check_game_state()
            else:
                # Clicked elsewhere - deselect or switch piece
                piece = self.board.squares[square]
                if piece != EMPTY and (piece & 8) == self.human_color:
                    self.selected_square = square
                    all_legal = self.board.get_legal_moves(self.human_color)
                    self.legal_moves = [move[1] for move in all_legal if move[0] == square]
                else:
                    self.selected_square = None
                    self.legal_moves = []

    # def draw_coach_panel(self):
    #     """Draw AI coach analysis panel."""
    #     if not self.coach or not self.coach_analysis:
    #         return
        
    #     y_offset = self.WINDOW_HEIGHT - 190
        
    #     # Panel background
    #     coach_rect = pygame.Rect(self.BOARD_SIZE + 5, y_offset, self.SIDEBAR - 10, 160)
    #     pygame.draw.rect(self.screen, (25, 35, 55), coach_rect, border_radius=8)
    #     pygame.draw.rect(self.screen, (80, 150, 220), coach_rect, 2, border_radius=8)
        
    #     # Title
    #     title = self.small_font.render("AI COACH:", True, (80, 180, 255))
    #     self.screen.blit(title, (self.BOARD_SIZE + 15, y_offset + 8))
        
    #     # Word-wrap analysis text
    #     words = self.coach_analysis.split()
    #     lines = []
    #     current = ""
    #     for word in words:
    #         test = current + " " + word if current else word
    #         if self.small_font.size(test)[0] < self.SIDEBAR - 30:
    #             current = test
    #         else:
    #             lines.append(current)
    #             current = word
    #     if current:
    #         lines.append(current)
        
    #     for i, line in enumerate(lines[:7]):
    #         text = self.small_font.render(line, True, (210, 210, 210))
    #         self.screen.blit(text, (self.BOARD_SIZE + 15, y_offset + 30 + i * 20))
    
    # def check_game_state(self):
    #     """Check for checkmate/stalemate."""
    #     legal_moves = self.board.get_legal_moves(self.board.current_player)
    #     if not legal_moves:
    #         self.game_over = True
    #         if self.board.is_in_check(self.board.current_player):
    #             winner = "Black" if self.board.current_player == WHITE else "White"
    #             self.result_message = f"Checkmate! {winner} wins!"
    #         else:
    #             self.result_message = "Stalemate! Draw!"
    
    def check_game_state(self):
        """Check for checkmate/stalemate."""
        legal_moves = self.board.get_legal_moves(self.board.current_player)
        if not legal_moves:
            self.game_over = True
            if self.board.is_in_check(self.board.current_player):
                winner = "Black" if self.board.current_player == WHITE else "White"
                self.result_message = f"Checkmate! {winner} wins!"
            else:
                self.result_message = "Stalemate! Draw!"
            
            # Get post-game analysis
            if self.coach and self.coach.active:
                self.coach_analysis = self.coach.post_game_review(
                    self.move_history, self.result_message
                )
    
    def draw_all(self):
        """Draw everything."""
        self.draw_board()
        self.draw_pieces()
        self.draw_sidebar()
    
    # def run(self):
    #     """Main game loop."""
    #     running = True
        
    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False
                
    #             elif event.type == pygame.MOUSEBUTTONDOWN:
    #                 x, y = pygame.mouse.get_pos()
    #                 square = self.get_square_from_click(x, y)
    #                 if square is not None:
    #                     self.handle_click(square)
                
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_r and self.game_over:
    #                     # Restart game
    #                     from board import Board
    #                     self.__init__(Board(), self.get_best_move)
            
    #         self.draw_all()
    #         pygame.display.flip()
    #         self.clock.tick(60)
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    square = self.get_square_from_click(x, y)
                    if square is not None:
                        self.handle_click(square)
                
                elif event.type == pygame.KEYDOWN:
                    # Toggle coach ON/OFF with 'C' key
                    if event.key == pygame.K_c and self.coach:
                        status = self.coach.toggle()
                        if status == "on":
                            self.coach_analysis = "Coach activated! Make a move."
                        else:
                            self.coach_analysis = ""
                    
                    # Restart game with 'R' key
                    elif event.key == pygame.K_r and self.game_over:
                        from board import Board
                        # Show post-game review if coach is active
                        if self.coach and self.coach.active:
                            review = self.coach.post_game_review(self.move_history, self.result_message)
                            self.coach_analysis = review
                            self.draw_all()
                            pygame.display.flip()
                            pygame.time.wait(5000)  # Show review for 5 seconds
                        self.__init__(Board(), self.get_best_move, self.coach)
            
            self.draw_all()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()    
        # pygame.quit()