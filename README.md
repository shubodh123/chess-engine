# ♟️ Chess Engine with AI Coach

A fully playable Python chess engine with a Pygame GUI, Minimax search with alpha-beta pruning, all special moves, and a live AI coaching system powered by the Google Gemini API that guides you through games without ever just handing you the answer.

---

## Features

- **Complete chess rules** — legal move generation for all pieces including castling, en passant, and pawn promotion
- **Minimax engine** with alpha-beta pruning and capture-first move ordering (plays at configurable depth)
- **Pygame GUI** — click-to-move interface with legal move highlighting, capture indicators, and a move history sidebar
- **AI Coach (Gemini-powered)** — positional hints after every move, pre-move blunder warnings, move evaluations, and a full post-game review
- **Piece images** — PNG piece set loaded from a `Pieces/` folder with unicode symbol fallback
- **Turn-aware board colors** — board tint shifts to reflect whose turn it is

---

## Project Structure

```
chess-engine/
│
├── main.py             # Entry point — wires board, engine, coach, and GUI together
├── board.py            # Board state, move execution, check detection, legal move filtering
├── move_generator.py   # Pseudo-legal move generation for all piece types
├── search.py           # Minimax with alpha-beta pruning and move ordering
├── evaluation.py       # Static position evaluator (material counting)
├── special_moves.py    # Castling, en passant, promotion logic
├── coach.py            # AI Coach — Gemini API integration for hints and analysis
├── gui.py              # Pygame GUI — board rendering, sidebar, coach panel, event loop
├── constants.py        # Piece codes, color flags, display symbols
├── convert_pieces.py   # One-time utility to convert SVG pieces to PNG
│
└── Pieces/             # PNG chess piece images (wK.png, bQ.png, etc.)
```

---

## How It Works

### Board Representation

Pieces are stored as integers in a flat 64-element list (`board.squares`), where each square index maps as `rank * 8 + file`. Piece identity is encoded in the lower 3 bits (type) and bit 3 (color):

```
WHITE = 0,  BLACK = 8
PAWN = 1, KNIGHT = 2, BISHOP = 3, ROOK = 4, QUEEN = 5, KING = 6

e.g.  WHITE_QUEEN = 5 | 0 = 5
      BLACK_KNIGHT = 2 | 8 = 10
```

Extracting type and color from any piece code:
```python
piece_type  = piece & 7   # lower 3 bits
piece_color = piece & 8   # bit 3
```

### Move Generation

`MoveGenerator` pre-computes knight and king destination tables at startup (since their moves are always the same regardless of board state). Sliding pieces (bishop, rook, queen) use a ray-casting loop that stops at the first blocker — capturing enemy pieces, stopping before friendly ones.

Pawn moves handle direction by color, double pushes from the starting rank, and diagonal captures separately.

### Legal Move Filtering

Pseudo-legal moves (moves that may leave the king in check) are filtered in `Board.get_legal_moves()` by making each move on the actual board, checking if the king is attacked, then undoing it. This is the simplest correct approach, though not the fastest possible.

### Search

Minimax with alpha-beta pruning (`search.py`). Captures are ordered before quiet moves to maximize pruning efficiency. Default search depth is 3 (responds in under a second on most hardware). Change the depth in `main.py`:

```python
engine_move = self.get_best_move(self.board, depth=3)  # increase for stronger play
```

### Evaluation

Currently material-only (`evaluation.py`) — counts piece values from White's perspective. Positive score favors White, negative favors Black.

```
Pawn=100  Knight=320  Bishop=330  Rook=500  Queen=900  King=20000
```

### AI Coach

`coach.py` uses the `google-genai` SDK to call `gemini-1.5-flash`. The board state is serialized to FEN notation before each call. The coach has three modes of interaction:

| Trigger | What happens |
|---|---|
| Before your move (warn mode) | Checks if the move you're about to play blunders material |
| After your move | Evaluates the move you just played in 1–2 sentences |
| After engine move | Gives a vague positional hint — no specific squares or pieces named |
| Game over | Full 4–5 sentence post-game review covering what decided the game |

The coach deliberately withholds the best move — it guides you toward the insight rather than giving it away, like a real coach would.

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/chess-engine.git
cd chess-engine
```

### 2. Install dependencies

```bash
pip install pygame google-genai Pillow svglib reportlab
```

### 3. Set up piece images

If you have SVG pieces in a `Pieces/` folder, convert them to PNG first:

```bash
python convert_pieces.py
```

This creates a `pieces_png/` folder. Move its contents into `Pieces/` and rename them to match the expected format: `wK.png`, `wQ.png`, `wR.png`, `wB.png`, `wN.png`, `wP.png`, `bK.png`, `bQ.png`, `bR.png`, `bB.png`, `bN.png`, `bP.png`.

If you skip this step, the engine falls back to unicode text symbols — everything still works, it just looks plainer.

### 4. Add your Gemini API key

Open `main.py` and replace the placeholder with your actual key:

```python
API_KEY = "your_gemini_api_key_here"
```

Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey). The free tier supports 15 requests/minute and 1 million tokens/day — more than enough for casual play.

### 5. Run

```bash
python main.py
```

---

## Controls

| Input | Action |
|---|---|
| **Click a piece** | Select it — legal moves appear as dots/circles |
| **Click a highlighted square** | Move the selected piece |
| **Click elsewhere** | Deselect, or switch to another piece |
| **C key** | Toggle AI Coach ON / OFF |
| **R key** (after game ends) | Restart — shows post-game review for 5 seconds first |
| **Close window** | Quit |

---

## Configuration

### Engine Strength

Edit the depth in `gui.py` inside `handle_click`:

```python
engine_move = self.get_best_move(self.board, depth=3)
# depth=2 → very fast, weaker
# depth=4 → noticeably slower, stronger
# depth=5+ → may take several seconds per move
```

### Coach Modes

Call `coach.set_mode()` before starting the GUI to change coaching behavior:

```python
coach.set_mode("hint")   # default — hints after every move
coach.set_mode("warn")   # also warns you before a bad move
coach.set_mode("full")   # maximum feedback
```

### Gemini Model

The coach uses `gemini-1.5-flash` by default (fast, free). To use a different model, edit `coach.py`:

```python
response = self.client.models.generate_content(
    model='gemini-2.0-flash-lite',  # or any other available model
    contents=prompt
)
```

---

## Troubleshooting

**Coach shows `[Coach offline: ClientError]`**

Your API key is invalid or the Gemini quota is exceeded. Check the terminal for the full error printed by the coach. Verify your key at aistudio.google.com.

**Coach shows nothing / old generic text**

Make sure the coach is active (`self.active = True` in `coach.py` — it starts active by default). If the panel shows `OFF (Press C)`, press C in-game to activate.

**Pieces show as letters instead of images**

The `Pieces/` folder is missing or the filenames don't match. The expected names are `wK.png`, `bQ.png`, etc. Run `convert_pieces.py` if starting from SVGs. Unicode fallback is automatic and the game is fully playable without images.

**Engine moves slowly**

Lower the search depth from 3 to 2 in `gui.py`. Alternatively, the evaluation function is purely material-based — adding piece-square tables would improve strength without needing a deeper search.

**Rate limit errors (429)**

The free Gemini tier allows 15 requests per minute. If you're getting 429 errors, add a small delay in `coach.py`'s `_ask_gemini` method:

```python
import time
time.sleep(1.5)
```

---

## Known Limitations

- No fifty-move rule or threefold repetition detection
- Pawn promotion always promotes to queen (no choice dialog)
- Evaluation is material-only — no positional scoring, no piece-square tables
- No time controls
- Engine plays only as Black (human always plays White)
- No game save / PGN export

---

## Possible Extensions

- Add piece-square tables to the evaluator for stronger positional play
- Iterative deepening with a time limit instead of fixed depth
- Transposition table (Zobrist hashing) to avoid re-evaluating the same positions
- Opening book (hardcoded or loaded from PGN)
- Player color selection at startup
- PGN export so you can load games into Lichess or Chess.com for analysis
- Promotion choice dialog for the GUI
- Sound effects on move, capture, and check

---

## Dependencies

| Package | Purpose |
|---|---|
| `pygame` | GUI rendering, event loop, input handling |
| `google-genai` | Gemini API client for the AI coach |
| `Pillow` | Image resizing when converting piece PNGs |
| `svglib` | SVG-to-PNG conversion (only needed for `convert_pieces.py`) |
| `reportlab` | Required by svglib for rendering (only for `convert_pieces.py`) |

---

## License

MIT License. Do whatever you want with it.
