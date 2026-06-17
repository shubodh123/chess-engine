# """
# AI Chess Coach - Uses Google Gemini to analyze positions
# """
# import google.generativeai as genai


# class ChessCoach:
#     def __init__(self, api_key):
#         genai.configure(api_key=api_key)
#         self.model = genai.GenerativeModel('gemini-1.5-flash')  # Free, fast model
#         print("AI Coach ready! (Gemini)")
    
#     def board_to_fen(self, board):
#         """Convert board to FEN notation."""
#         fen = ""
#         for rank in range(7, -1, -1):
#             empty = 0
#             for file in range(8):
#                 square = rank * 8 + file
#                 piece = board.squares[square]
                
#                 if piece == 0:
#                     empty += 1
#                 else:
#                     if empty > 0:
#                         fen += str(empty)
#                         empty = 0
#                     piece_map = {
#                         1: 'P', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K',
#                         9: 'p', 10: 'n', 11: 'b', 12: 'r', 13: 'q', 14: 'k'
#                     }
#                     fen += piece_map.get(piece, '?')
#             if empty > 0:
#                 fen += str(empty)
#             if rank > 0:
#                 fen += '/'
        
#         fen += ' w' if board.current_player == 8 else ' b'
#         fen += ' - - 0 1'  # Simplified FEN
#         return fen
    
#     def analyze_position(self, board, last_move=None):
#         """Get AI analysis of the current position."""
#         fen = self.board_to_fen(board)
        
#         move_text = ""
#         if last_move:
#             from_sq, to_sq = last_move
#             files = 'abcdefgh'
#             move_text = f"\nLast move: {files[from_sq%8]}{from_sq//8+1} to {files[to_sq%8]}{to_sq//8+1}"
        
#         prompt = f"""Act as a chess coach. Analyze this position briefly:
# {fen}{move_text}

# Give me:
# 1. Who's better and why (one line)
# 2. Best plan for the current player (one line)
# 3. Any tactic available (one line, or say "none")
# Keep it under 80 words. Be direct."""
        
#         try:
#             response = self.model.generate_content(prompt)
#             return response.text
#         except Exception as e:
#             return f"Coach: {e}"
    
#     def explain_move(self, board, move):
#         """Explain a move that was just played."""
#         fen = self.board_to_fen(board)
#         from_sq, to_sq = move
#         files = 'abcdefgh'
#         move_str = f"{files[from_sq%8]}{from_sq//8+1} to {files[to_sq%8]}{to_sq//8+1}"
        
#         prompt = f"""As a chess coach, explain this move briefly:
# Position FEN: {fen}
# Move played: {move_str}

# Is it good? Why? (2-3 sentences max, under 60 words)"""
        
#         try:
#             response = self.model.generate_content(prompt)
#             return response.text
#         except Exception as e:
#             return f"Coach: {e}"


# """
# AI Chess Coach - Uses Google Gemini to analyze positions
# """
# from google import genai


# class ChessCoach:
#     def __init__(self, api_key):
#         self.client = genai.Client(api_key=api_key)
#         print("AI Coach ready! (Gemini)")
    
#     def board_to_fen(self, board):
#         """Convert board to FEN notation."""
#         fen = ""
#         for rank in range(7, -1, -1):
#             empty = 0
#             for file in range(8):
#                 square = rank * 8 + file
#                 piece = board.squares[square]
                
#                 if piece == 0:
#                     empty += 1
#                 else:
#                     if empty > 0:
#                         fen += str(empty)
#                         empty = 0
#                     piece_map = {
#                         1: 'P', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K',
#                         9: 'p', 10: 'n', 11: 'b', 12: 'r', 13: 'q', 14: 'k'
#                     }
#                     fen += piece_map.get(piece, '?')
#             if empty > 0:
#                 fen += str(empty)
#             if rank > 0:
#                 fen += '/'
        
#         fen += ' w' if board.current_player == 8 else ' b'
#         fen += ' - - 0 1'
#         return fen
    
#     def analyze_position(self, board, last_move=None):
#         """Get AI analysis of the current position."""
#         fen = self.board_to_fen(board)
        
#         move_text = ""
#         if last_move:
#             from_sq, to_sq = last_move
#             files = 'abcdefgh'
#             move_text = f"\nLast move: {files[from_sq%8]}{from_sq//8+1} to {files[to_sq%8]}{to_sq//8+1}"
        
#         prompt = f"""Act as a chess coach. Analyze this position briefly:
# {fen}{move_text}

# Give me:
# 1. Who's better and why (one line)
# 2. Best plan for the current player (one line)
# 3. Any tactic available (one line, or say "none")
# Keep it under 80 words. Be direct."""
        
#         try:
#             response = self.client.models.generate_content(
#                 model='gemini-1.5-flash',
#                 contents=prompt
#             )
#             return response.text
#         except Exception as e:
#             return f"Coach: {e}"
    
#     def explain_move(self, board, move):
#         """Explain a move that was just played."""
#         fen = self.board_to_fen(board)
#         from_sq, to_sq = move
#         files = 'abcdefgh'
#         move_str = f"{files[from_sq%8]}{from_sq//8+1} to {files[to_sq%8]}{to_sq//8+1}"
        
#         prompt = f"""As a chess coach, explain this move briefly:
# Position FEN: {fen}
# Move played: {move_str}

# Is it good? Why? (2-3 sentences max, under 60 words)"""
        
#         try:
#             response = self.client.models.generate_content(
#                 model='gemini-1.5-flash',
#                 contents=prompt
#             )
#             return response.text
#         except Exception as e:
#             return f"Coach: {e}"


"""
# AI Chess Coach - Guides without spoiling, analyzes at game end
# """
# from google import genai


# class ChessCoach:
#     def __init__(self, api_key):
#         self.client = genai.Client(api_key=api_key)
#         self.active = True
#         self.mode = "hint"  # hint, warn, full
#         self.game_analysis = None
#         print("AI Coach ready! Press 'C' in game to toggle ON/OFF")
    
#     def toggle(self):
#         """Turn coach ON/OFF."""
#         self.active = not self.active
#         return "on" if self.active else "off"
    
#     def set_mode(self, mode):
#         """Change coaching mode."""
#         self.mode = mode
    
#     def board_to_fen(self, board):
#         """Convert board to FEN notation."""
#         fen = ""
#         for rank in range(7, -1, -1):
#             empty = 0
#             for file in range(8):
#                 square = rank * 8 + file
#                 piece = board.squares[square]
                
#                 if piece == 0:
#                     empty += 1
#                 else:
#                     if empty > 0:
#                         fen += str(empty)
#                         empty = 0
#                     piece_map = {
#                         1: 'P', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K',
#                         9: 'p', 10: 'n', 11: 'b', 12: 'r', 13: 'q', 14: 'k'
#                     }
#                     fen += piece_map.get(piece, '?')
#             if empty > 0:
#                 fen += str(empty)
#             if rank > 0:
#                 fen += '/'
        
#         fen += ' w' if board.current_player == 8 else ' b'
#         fen += ' - - 0 1'
#         return fen
    
#     def get_hint(self, board):
#         """Give a vague hint — doesn't reveal best move."""
#         if not self.active:
#             return None
        
#         fen = self.board_to_fen(board)
        
#         prompt = f"""You are a chess coach. Give ONE vague hint to the current player.
# Position: {fen}

# Rules:
# - Do NOT say which specific piece to move
# - Do NOT say which square to move to
# - Give general guidance like "think about the center" or "your king looks exposed"
# - One sentence only, under 15 words
# - Be encouraging

# Hint:"""
        
#         try:
#             response = self.client.models.generate_content(
#                 model='gemini-1.5-flash',
#                 contents=prompt
#             )
#             return response.text.strip()
#         except:
#             return "Focus on piece development and center control."
    
#     def warn_before_move(self, board, attempted_move):
#         """Warn if a move seems bad — called BEFORE move is made."""
#         if not self.active or self.mode != "warn":
#             return None
        
#         fen = self.board_to_fen(board)
#         from_sq, to_sq = attempted_move
#         files = 'abcdefgh'
#         move_str = f"{files[from_sq%8]}{from_sq//8+1} to {files[to_sq%8]}{to_sq//8+1}"
        
#         prompt = f"""You are a chess coach. A student is about to play {move_str}.
# Position: {fen}

# Quickly:
# 1. If this move blunders a piece or loses material, say "WARNING:" and explain briefly
# 2. If it's a decent move, just say "OK"
# 3. Under 30 words max

# Response:"""
        
#         try:
#             response = self.client.models.generate_content(
#                 model='gemini-1.5-flash',
#                 contents=prompt
#             )
#             return response.text.strip()
#         except:
#             return None
    
#     def analyze_move(self, board, move):
#         """Briefly comment on a move just played."""
#         if not self.active:
#             return None
        
#         fen = self.board_to_fen(board)
#         from_sq, to_sq = move
#         files = 'abcdefgh'
#         move_str = f"{files[from_sq%8]}{from_sq//8+1} to {files[to_sq%8]}{to_sq//8+1}"
        
#         prompt = f"""Chess coach here. The player just played {move_str}.
# Position after move: {fen}

# Give a 2-sentence evaluation. Be constructive but honest. Under 50 words total.

# Analysis:"""
        
#         try:
#             response = self.client.models.generate_content(
#                 model='gemini-1.5-flash',
#                 contents=prompt
#             )
#             return response.text.strip()
#         except:
#             return "Interesting move. Let's see how the opponent responds."
    
#     def post_game_review(self, move_history, result_message):
#         """Full game analysis after game ends."""
#         moves = ", ".join(move_history[-20:])  # Last 20 moves
#         result = result_message
        
#         prompt = f"""You are a chess coach reviewing a completed game.
# Result: {result}
# Last moves: {moves}

# Provide a 4-5 sentence game review:
# 1. What decided the game?
# 2. One thing the winner did well
# 3. One thing the loser should work on
# 4. An encouraging final note

# Under 100 words total.

# Review:"""
        
#         try:
#             response = self.client.models.generate_content(
#                 model='gemini-1.5-flash',
#                 contents=prompt
#             )
#             return response.text.strip()
#         except:
#             return "Great game! Review the critical moments to improve next time."

"""
AI Chess Coach - Uses Google Gemini (google-genai SDK) to guide players.
"""
from google import genai


class ChessCoach:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.active = True   # FIX: start active so coach works immediately
        self.mode = "hint"
        print("AI Coach ready! (Gemini) Press 'C' to toggle ON/OFF")

    def toggle(self):
        self.active = not self.active
        return "on" if self.active else "off"

    def set_mode(self, mode):
        self.mode = mode

    def board_to_fen(self, board):
        """Convert board state to FEN notation."""
        fen = ""
        for rank in range(7, -1, -1):
            empty = 0
            for file in range(8):
                square = rank * 8 + file
                piece = board.squares[square]
                if piece == 0:
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    piece_map = {
                        1: 'P', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K',
                        9: 'p', 10: 'n', 11: 'b', 12: 'r', 13: 'q', 14: 'k'
                    }
                    fen += piece_map.get(piece, '?')
            if empty > 0:
                fen += str(empty)
            if rank > 0:
                fen += '/'
        fen += ' w' if board.current_player == 8 else ' b'
        fen += ' - - 0 1'
        return fen

    def _ask_gemini(self, prompt, max_output_tokens=120):
        """Send a prompt to Gemini and return the text, with visible error on failure."""
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            # Surface the real error instead of silently swallowing it
            print(f"[Coach ERROR] Gemini call failed: {e}")
            return f"[Coach offline: {type(e).__name__}]"

    def get_hint(self, board):
        """Give a vague positional hint — does NOT reveal the best move."""
        if not self.active:
            return None

        fen = self.board_to_fen(board)
        player = "White" if board.current_player == 8 else "Black"

        prompt = f"""You are a chess coach helping {player}.
Position (FEN): {fen}

Give ONE short positional hint under 15 words.
Rules:
- Do NOT name a specific piece or destination square
- Be specific to THIS position (not generic advice like "develop pieces")
- Be encouraging

Hint:"""
        return self._ask_gemini(prompt)

    def warn_before_move(self, board, attempted_move):
        """Warn if a move looks bad — called BEFORE the move is made."""
        if not self.active or self.mode != "warn":
            return None

        fen = self.board_to_fen(board)
        from_sq, to_sq = attempted_move
        files = 'abcdefgh'
        move_str = f"{files[from_sq % 8]}{from_sq // 8 + 1} to {files[to_sq % 8]}{to_sq // 8 + 1}"

        prompt = f"""Chess coach reviewing a move about to be played: {move_str}
Position (FEN): {fen}

Reply ONLY with:
- "OK" if the move is reasonable
- "WARNING: [reason under 20 words]" if it clearly blunders material

Response:"""
        return self._ask_gemini(prompt, max_output_tokens=60)

    def analyze_move(self, board, move):
        """Comment on a move just played."""
        if not self.active:
            return None

        fen = self.board_to_fen(board)
        from_sq, to_sq = move
        files = 'abcdefgh'
        move_str = f"{files[from_sq % 8]}{from_sq // 8 + 1} to {files[to_sq % 8]}{to_sq // 8 + 1}"

        prompt = f"""You are a chess coach. The player just played {move_str}.
Position after move (FEN): {fen}

Give a 1-2 sentence honest evaluation of this specific move.
Do not suggest what to play next. Under 40 words.

Analysis:"""
        return self._ask_gemini(prompt)

    def post_game_review(self, move_history, result_message):
        """Full game review after game ends."""
        moves = ", ".join(move_history[-20:])

        prompt = f"""You are a chess coach reviewing a completed game.
Result: {result_message}
Last moves: {moves}

Write a 4-5 sentence review covering:
1. What decided the game
2. One thing the winner did well
3. One thing the loser should work on
4. An encouraging closing note

Under 100 words.

Review:"""
        return self._ask_gemini(prompt, max_output_tokens=200)