"""
Test Script - Shows LaTeX generation without requiring Tectonic
This script demonstrates what LaTeX code would be generated.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from chess_generator import ChessDiagramGenerator


def show_latex_for_single_diagram():
    """Show LaTeX code for a single diagram"""
    print("=" * 70)
    print("EXAMPLE 1: Single Diagram LaTeX Code")
    print("=" * 70)
    
    generator = ChessDiagramGenerator(verbose=False)
    
    # Generate LaTeX content (without compiling)
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    latex_content = generator._generate_latex_preamble()
    latex_content += "\\section*{Starting Position}\n\n"
    latex_content += f"\\chessboard[setfen={fen}, boardfontsize=1.5em, width=3in]\n\n"
    latex_content += "\\begin{center}\\textit{The initial setup for a game of chess}\\end{center}\n\n"
    latex_content += generator._generate_latex_postamble()
    
    print(latex_content)
    print("\n" + "=" * 70)


def show_latex_for_annotated_game():
    """Show LaTeX code for an annotated game"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Annotated Game LaTeX Code")
    print("=" * 70)
    
    try:
        import chess.pgn
        from io import StringIO
        
        pgn_text = """[Event "Scholar's Mate"]
[White "Student"]
[Black "Beginner"]
[Result "1-0"]

1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7# 1-0"""
        
        pgn = StringIO(pgn_text)
        game = chess.pgn.read_game(pgn)
        
        generator = ChessDiagramGenerator(verbose=False)
        latex_content = generator._generate_latex_preamble()
        
        # Add game header
        white = game.headers.get("White", "?")
        black = game.headers.get("Black", "?")
        result = game.headers.get("Result", "*")
        
        latex_content += f"\\section*{{{white} vs {black}}}\n\n"
        latex_content += f"\\textbf{{Result:}} {result}\n\n"
        
        # Add game
        latex_content += "\\newchessgame\n"
        latex_content += "\\mainline{"
        
        moves = []
        board = game.board()
        for move in game.mainline_moves():
            moves.append(board.san(move))
            board.push(move)
        
        for i, move in enumerate(moves):
            if i % 2 == 0:
                latex_content += f"{i//2 + 1}. "
            latex_content += move + " "
        
        latex_content += "}\n\n"
        latex_content += "\\subsection*{Final Position}\n\n"
        latex_content += "\\chessboard[boardfontsize=1.5em]\n\n"
        latex_content += generator._generate_latex_postamble()
        
        print(latex_content)
        print("\n" + "=" * 70)
        
    except ImportError:
        print("\nNote: python-chess not installed. Install with: pip install chess")
        print("Showing template without actual game parsing...\n")
        
        latex_template = """\\documentclass[11pt]{article}
\\usepackage{xskak}
\\usepackage{chessboard}
\\usepackage[margin=1in]{geometry}

\\begin{document}

\\section*{Student vs Beginner}

\\textbf{Result:} 1-0

\\newchessgame
\\mainline{1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7#}

\\subsection*{Final Position}

\\chessboard[boardfontsize=1.5em]

\\end{document}"""
        print(latex_template)
        print("\n" + "=" * 70)


def show_fen_examples():
    """Show various FEN positions and their use cases"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: FEN Notation Examples")
    print("=" * 70)
    
    examples = [
        {
            "name": "Starting Position",
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        },
        {
            "name": "Back Rank Mate Puzzle",
            "fen": "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1"
        },
        {
            "name": "Endgame: King and Pawn vs King",
            "fen": "8/8/8/4k3/8/4K3/4P3/8 w - - 0 1"
        },
        {
            "name": "The Immortal Game (critical moment)",
            "fen": "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 w - - 1 12"
        },
        {
            "name": "Sicilian Dragon Variation",
            "fen": "r2q1rk1/1p1bbppp/p2p1n2/n3p3/4P3/2NP1NP1/PPB2PBP/R2Q1RK1 w - - 0 12"
        }
    ]
    
    print("\nTo use these positions, create diagrams like this:\n")
    print('generator.generate_single_diagram(')
    print('    fen="[FEN_STRING]",')
    print('    output_pdf="output.pdf",')
    print('    title="[TITLE]"')
    print(')\n')
    
    for ex in examples:
        print(f"\n{ex['name']}:")
        print(f"  FEN: {ex['fen']}")


def show_integration_example():
    """Show how to integrate into a larger application"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Integration into Your Application")
    print("=" * 70)
    
    code = '''
# In your_application.py

from pathlib import Path
from chess_generator import ChessDiagramGenerator

class ChessBookPublisher:
    """Example: Publishing a chess book with multiple chapters"""
    
    def __init__(self, book_title):
        self.title = book_title
        self.generator = ChessDiagramGenerator(verbose=True)
        self.output_dir = Path("books") / book_title.replace(" ", "_")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def add_opening_chapter(self, opening_name, games):
        """Add a chapter on a specific opening"""
        chapter_dir = self.output_dir / "chapters"
        chapter_dir.mkdir(exist_ok=True)
        
        for i, game in enumerate(games):
            output_file = chapter_dir / f"{opening_name}_{i+1}.pdf"
            self.generator.generate_annotated_game(
                pgn_content=game,
                output_pdf=output_file,
                show_final_position=True
            )
    
    def add_puzzle_section(self, puzzles):
        """Add tactical puzzles"""
        puzzle_dir = self.output_dir / "puzzles"
        puzzle_dir.mkdir(exist_ok=True)
        
        for i, (fen, title) in enumerate(puzzles):
            output_file = puzzle_dir / f"puzzle_{i+1}.pdf"
            self.generator.generate_single_diagram(
                fen=fen,
                output_pdf=output_file,
                title=title,
                caption=f"Puzzle #{i+1}"
            )

# Usage
publisher = ChessBookPublisher("My Chess Repertoire")

# Add games for each opening
sicilian_games = [pgn1, pgn2, pgn3]
publisher.add_opening_chapter("Sicilian_Defense", sicilian_games)

# Add puzzles
puzzles = [
    ("6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1", "Back Rank Mate"),
    ("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4", "Fork the King")
]
publisher.add_puzzle_section(puzzles)
'''
    
    print(code)
    print("\n" + "=" * 70)


def main():
    """Run all demonstration examples"""
    print("\n" + "=" * 70)
    print("CHESS DIAGRAM GENERATOR - LaTeX Code Examples")
    print("=" * 70)
    print("\nThis script shows the LaTeX code that would be generated.")
    print("To actually compile to PDF, you need Tectonic installed.")
    print("See README.md for installation instructions.\n")
    
    show_latex_for_single_diagram()
    show_latex_for_annotated_game()
    show_fen_examples()
    show_integration_example()
    
    print("\n" + "=" * 70)
    print("For full working examples with PDF generation:")
    print("  python examples/all_examples.py")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
