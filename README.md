
<img width="255" height="330" alt="example4_opera_game" src="https://github.com/user-attachments/assets/8cc036a8-44ae-4044-ae82-9c941787b100" />

# Chess Diagram Generator

A cross-platform Python application for generating publication-ready chess diagrams and annotated games using LaTeX.

**✅ Tested and working with TeX Live on Linux, macOS, and Windows**

## Features

- ✅ Generate single diagrams from FEN notation
- ✅ Create complete annotated games with move-by-move notation
- ✅ Insert diagrams at specific moves in a game
- ✅ High-quality PDF output suitable for books and publications
- ✅ Cross-platform (Windows, Linux, macOS)
- ✅ Automatic LaTeX engine detection (pdflatex, xelatex, or Tectonic)
- ✅ Works with standard TeX Live installations
- ✅ Supports immutable Linux systems via distrobox/toolbox

## Quick Start

### 1. Setup

```bash
# Clone or download this repository
cd chess_diagram_app

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install LaTeX (Required)

This application requires a LaTeX distribution with chess packages.

#### OPTION A: TeX Live (Recommended - tested and working)

TeX Live is the most reliable option and works out of the box.

**Fedora/RHEL:**
```bash
sudo dnf install texlive-scheme-basic texlive-xskak texlive-chessboard texlive-parskip
```

**Ubuntu/Debian:**
```bash
sudo apt-get install texlive-games texlive-latex-extra
```

**Arch Linux:**
```bash
sudo pacman -S texlive-games
```

**macOS:**
```bash
# Full MacTeX (~4GB)
brew install --cask mactex

# Or BasicTeX + packages (~400MB)
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install xskak chessboard parskip
```

**Windows:**
- Download and install [MiKTeX](https://miktex.org/download)
- Packages will be installed automatically on first use

**Note for immutable systems (Fedora Silverblue/Kinoite):**
```bash
# Use distrobox or toolbox
toolbox create chess-dev
toolbox enter chess-dev
sudo dnf install texlive-scheme-basic texlive-xskak texlive-chessboard texlive-parskip
pip install chess
```
### 3. Verify Setup

```bash
# Run the verification script
python3 verify_setup.py
```

This will check:
- Python version and dependencies
- LaTeX engine availability (pdflatex/xelatex/tectonic)
- Required LaTeX packages
- Test diagram generation

**Expected output:**
```
✓ PASS: Python 3.7+
✓ PASS: python-chess library
✓ PASS: LaTeX engine (pdflatex)
✓ PASS: LaTeX chess packages
✓ PASS: Diagram generation
```

### 4. Run Examples

```bash
# Run all examples
python examples/all_examples.py

# Check output directory for generated PDFs
ls output/
```

### 3. Use in Your Code

```python
from chess_generator import ChessDiagramGenerator

generator = ChessDiagramGenerator(verbose=True)

# Generate a single diagram
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
generator.generate_single_diagram(
    fen=fen,
    output_pdf="output/my_diagram.pdf",
    title="Starting Position",
    caption="The initial chess position"
)
```

## Directory Structure

```
chess_diagram_app/
├── bin/
│   ├── linux/              # Tectonic binary for Linux
│   ├── windows/            # Tectonic binary for Windows
│   ├── macos/              # Tectonic binary for macOS
│   └── DOWNLOAD_TECTONIC.md
├── examples/
│   └── all_examples.py     # Complete usage examples
├── output/                 # Generated PDFs go here
├── chess_generator.py      # Main application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## API Reference

### ChessDiagramGenerator

Main class for generating chess diagrams.

#### `generate_single_diagram(fen, output_pdf, title=None, caption=None, board_size="3in")`

Generate a single diagram from FEN notation.

**Parameters:**
- `fen` (str): FEN string representing the position
- `output_pdf` (Path): Where to save the PDF
- `title` (str, optional): Title above the diagram
- `caption` (str, optional): Caption below the diagram
- `board_size` (str): Size of board (e.g., "3in", "10cm")

**Returns:** `bool` - True if successful

**Example:**
```python
generator = ChessDiagramGenerator(verbose=True)
generator.generate_single_diagram(
    fen="r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
    output_pdf="output/position.pdf",
    title="Sicilian Defense",
    caption="After 1.e4 c5 2.Nf3 Nc6"
)
```

#### `generate_annotated_game(pgn_content, output_pdf, diagrams_at_moves=None, show_final_position=True)`

Generate a complete annotated game with optional diagrams.

**Parameters:**
- `pgn_content` (str): PGN format game
- `output_pdf` (Path): Where to save the PDF
- `diagrams_at_moves` (List[int], optional): Move numbers for diagrams (0-indexed)
- `show_final_position` (bool): Whether to show final position

**Returns:** `bool` - True if successful

**Example:**
```python
pgn = """[Event "World Championship"]
[White "Kasparov"]
[Black "Karpov"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 1-0"""

generator.generate_annotated_game(
    pgn_content=pgn,
    output_pdf="output/game.pdf",
    diagrams_at_moves=[4, 8],  # Show diagrams after moves 5 and 9
    show_final_position=True
)
```

#### `generate_diagram_at_move(pgn_content, move_number, output_pdf, title=None)`

Extract and generate a diagram at a specific move.

**Parameters:**
- `pgn_content` (str): PGN format game
- `move_number` (int): Move number to extract (0-indexed, half-moves)
- `output_pdf` (Path): Where to save the PDF
- `title` (str, optional): Title for the diagram

**Returns:** `bool` - True if successful

**Example:**
```python
generator.generate_diagram_at_move(
    pgn_content=pgn,
    move_number=10,  # After the 11th move (0-indexed)
    output_pdf="output/move10.pdf",
    title="Critical Position"
)
```

## Examples

### Example 1: Basic Diagram

```python
from chess_generator import ChessDiagramGenerator
from pathlib import Path

generator = ChessDiagramGenerator(verbose=True)

# The Immortal Game position
fen = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 w - - 1 12"

generator.generate_single_diagram(
    fen=fen,
    output_pdf=Path("immortal_game.pdf"),
    title="The Immortal Game",
    caption="After 11...Nxf3+ - Both rooks sacrificed!",
    board_size="4in"
)
```

### Example 2: Annotated Game with Diagrams

```python
pgn = """[Event "Opera Game"]
[Site "Paris"]
[Date "1858.??.??"]
[White "Paul Morphy"]
[Black "Duke Karl and Count Isouard"]
[Result "1-0"]

1. e4 e5 2. Nf3 d6 3. d4 Bg4 4. dxe5 Bxf3 5. Qxf3 dxe5 
6. Bc4 Nf6 7. Qb3 Qe7 8. Nc3 c6 9. Bg5 b5 10. Nxb5 cxb5 
11. Bxb5+ Nbd7 12. O-O-O Rd8 13. Rxd7 Rxd7 14. Rd1 Qe6 
15. Bxd7+ Nxd7 16. Qb8+ Nxb8 17. Rd8# 1-0"""

generator.generate_annotated_game(
    pgn_content=pgn,
    output_pdf=Path("opera_game.pdf"),
    diagrams_at_moves=[10, 15],  # After moves 11 and 16
    show_final_position=True
)
```

### Example 3: Puzzle

```python
# White to move and win
fen = "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1"

generator.generate_single_diagram(
    fen=fen,
    output_pdf=Path("puzzle.pdf"),
    title="Puzzle: White to Move and Win",
    caption="Find the back rank mate!"
)
```

## Customization

You can customize the LaTeX output by modifying the `ChessDiagramGenerator` class:

- Board size and styling
- Piece sets
- Page margins
- Typography

Example:
```python
# In chess_generator.py, modify _generate_latex_preamble():
\setchessboard{
    showmover=true,        # Show whose turn it is
    pgfstyle=color,        # Different square highlighting
    boardfontsize=2em,     # Larger pieces
    color=blue             # Highlight color
}
```

## Troubleshooting

### Quick Fix for Most Issues

Run the verification script to diagnose problems:

```bash
python3 verify_setup.py
```

### Common Issues

#### "File 'xskak.sty' not found"

**Cause:** LaTeX packages need to be downloaded on first use.

**Solution:**
1. Ensure internet connection
2. Run `python3 verify_setup.py` (downloads packages automatically)
3. Wait 30-60 seconds for download to complete
4. Try again

After first successful run, the app works offline.

#### "Tectonic not found" Error

**Solution:** Install Tectonic:
```bash
# macOS/Linux with Homebrew
brew install tectonic

# Fedora
sudo dnf install tectonic

# Or download binaries to bin/{platform}/ - see bin/DOWNLOAD_TECTONIC.md
```

#### "No module named 'chess'"

**Solution:** Install python-chess:
```bash
pip install -r requirements.txt
```

### Detailed Troubleshooting

For comprehensive troubleshooting including:
- Offline usage
- Proxy/firewall configuration
- Platform-specific issues (Windows, macOS, Linux)
- LaTeX package cache management
- CI/CD and Docker setup

See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## Dependencies

- **Python 3.7+**
- **python-chess**: For PGN parsing and FEN manipulation
- **Tectonic**: LaTeX engine (bundled or system-installed)

## License

This application is provided as-is for educational and publication purposes.

## Credits

- **Tectonic**: Modern, self-contained TeX/LaTeX engine
- **xskak**: LaTeX package for chess typesetting
- **python-chess**: Chess library for Python

## Contributing

Feel free to submit issues and enhancement requests!

## Support

For issues related to:
- Tectonic: https://github.com/tectonic-typesetting/tectonic
- python-chess: https://python-chess.readthedocs.io/
- This application: Open an issue in this repository
