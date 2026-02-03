# Quick Start Guide

## 5-Minute Setup

### Step 1: Install LaTeX

**Fedora/RHEL:**
```bash
sudo dnf install texlive-scheme-basic texlive-xskak texlive-chessboard texlive-parskip
```

**Ubuntu/Debian:**
```bash
sudo apt-get install texlive-games texlive-latex-extra
```

**macOS:**
```bash
# Quick option: BasicTeX (~400MB)
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install xskak chessboard parskip
```

**Windows:**
- Download [MiKTeX](https://miktex.org/download) and install
- Chess packages install automatically on first use

**Immutable Linux (Silverblue/Kinoite):**
```bash
toolbox create chess-dev
toolbox enter chess-dev
sudo dnf install texlive-scheme-basic texlive-xskak texlive-chessboard texlive-parskip
```

### Step 2: Install Python Package

```bash
pip install chess
```

### Step 3: Test It

```bash
# See what LaTeX would be generated (no Tectonic needed)
python demo_latex_output.py

# Generate actual PDFs (requires Tectonic)
python examples/all_examples.py
```

## Your First Diagram

Create a file `my_diagram.py`:

```python
from chess_generator import ChessDiagramGenerator
from pathlib import Path

generator = ChessDiagramGenerator(verbose=True)

# Create a diagram
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
generator.generate_single_diagram(
    fen=fen,
    output_pdf=Path("my_first_diagram.pdf"),
    title="My First Chess Diagram!"
)
```

Run it:
```bash
python my_diagram.py
```

Check the output: `my_first_diagram.pdf`

## Your First Annotated Game

```python
from chess_generator import ChessDiagramGenerator
from pathlib import Path

generator = ChessDiagramGenerator(verbose=True)

pgn = """[Event "My Game"]
[White "Me"]
[Black "Opponent"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O 1-0"""

generator.generate_annotated_game(
    pgn_content=pgn,
    output_pdf=Path("my_game.pdf"),
    show_final_position=True
)
```

## Common Tasks

### Generate Multiple Diagrams from a List

```python
positions = [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "Starting"),
    ("6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1", "Puzzle1"),
]

for fen, name in positions:
    generator.generate_single_diagram(
        fen=fen,
        output_pdf=Path(f"{name}.pdf")
    )
```

### Process PGN Files in Bulk

```python
import glob

for pgn_file in glob.glob("games/*.pgn"):
    with open(pgn_file) as f:
        pgn_content = f.read()
    
    output_name = Path(pgn_file).stem + ".pdf"
    generator.generate_annotated_game(
        pgn_content=pgn_content,
        output_pdf=Path("output") / output_name
    )
```

## Troubleshooting

**"No LaTeX engine found"**
```bash
# Verify pdflatex is installed
which pdflatex

# If not found, install TeX Live (see Step 1 above)
```

**"No module named 'chess'"**
```bash
pip install chess
```

**"File 'xskak.sty' not found"**
- Install chess LaTeX packages (see Step 1 above)
- On Ubuntu/Debian: `sudo apt-get install texlive-games`
- On Fedora: `sudo dnf install texlive-xskak texlive-chessboard`

**LaTeX compilation errors**
- Run with `verbose=True` to see details
- Check that FEN string is valid
- Ensure PGN is properly formatted
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed help

## Next Steps

- Read `README.md` for full documentation
- Check `examples/all_examples.py` for more examples
- See `demo_latex_output.py` to understand the LaTeX being generated
