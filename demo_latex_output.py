"""
Standalone Demo - Shows LaTeX generation without requiring Tectonic
This demonstrates the LaTeX code that would be generated.
"""


def generate_latex_preamble():
    """Standard LaTeX preamble for chess documents"""
    return r"""\documentclass[11pt]{article}
\usepackage{xskak}
\usepackage{chessboard}
\usepackage[margin=1in]{geometry}
\usepackage[utf8]{inputenc}
\usepackage{parskip}

% Custom chess board styling
\setchessboard{
    showmover=false,
    pgfstyle=border
}

\begin{document}
"""


def generate_latex_postamble():
    """Standard LaTeX postamble"""
    return r"""
\end{document}
"""


def demo_single_diagram():
    """Show LaTeX code for a single diagram"""
    print("=" * 70)
    print("EXAMPLE 1: Single Diagram - Starting Position")
    print("=" * 70 + "\n")
    
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    latex_content = generate_latex_preamble()
    latex_content += "\\section*{Chess Starting Position}\n\n"
    latex_content += f"\\chessboard[setfen={fen}, boardfontsize=1.5em, width=3in]\n\n"
    latex_content += "\\begin{center}\\textit{The initial setup for a game of chess}\\end{center}\n\n"
    latex_content += generate_latex_postamble()
    
    print(latex_content)
    print("=" * 70 + "\n")


def demo_tactical_puzzle():
    """Show LaTeX for a tactical puzzle"""
    print("=" * 70)
    print("EXAMPLE 2: Tactical Puzzle - Back Rank Mate")
    print("=" * 70 + "\n")
    
    fen = "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1"
    
    latex_content = generate_latex_preamble()
    latex_content += "\\section*{Puzzle: White to Move and Win}\n\n"
    latex_content += f"\\chessboard[setfen={fen}, boardfontsize=1.5em, width=3.5in]\n\n"
    latex_content += "\\begin{center}\\textit{Find the back rank mate in 1 move!}\\end{center}\n\n"
    latex_content += generate_latex_postamble()
    
    print(latex_content)
    print("=" * 70 + "\n")


def demo_annotated_game():
    """Show LaTeX for an annotated game"""
    print("=" * 70)
    print("EXAMPLE 3: Annotated Game - Scholar's Mate")
    print("=" * 70 + "\n")
    
    latex_content = generate_latex_preamble()
    
    # Game header
    latex_content += "\\section*{Student vs Beginner}\n\n"
    latex_content += "\\textbf{Event:} Scholar's Mate Example\\\\\n"
    latex_content += "\\textbf{Result:} 1-0\n\n"
    
    # Game notation
    latex_content += "\\newchessgame\n"
    latex_content += "\\mainline{1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7#}\n\n"
    
    # Final position
    latex_content += "\\subsection*{Final Position}\n\n"
    latex_content += "\\chessboard[boardfontsize=1.5em]\n\n"
    
    latex_content += generate_latex_postamble()
    
    print(latex_content)
    print("=" * 70 + "\n")


def demo_complex_game_with_diagrams():
    """Show LaTeX for a game with multiple diagrams"""
    print("=" * 70)
    print("EXAMPLE 4: Complex Game with Multiple Diagrams")
    print("=" * 70 + "\n")
    
    latex_content = generate_latex_preamble()
    
    # Game header
    latex_content += "\\section*{Paul Morphy vs Duke Karl / Count Isouard}\n\n"
    latex_content += "\\textbf{Event:} Opera Game\\\\\n"
    latex_content += "\\textbf{Site:} Paris\\\\\n"
    latex_content += "\\textbf{Date:} 1858\\\\\n"
    latex_content += "\\textbf{Result:} 1-0\n\n"
    
    # First part of game
    latex_content += "\\newchessgame\n"
    latex_content += "\\mainline{1. e4 e5 2. Nf3 d6 3. d4 Bg4 4. dxe5 Bxf3 5. Qxf3 dxe5 "
    latex_content += "6. Bc4 Nf6 7. Qb3 Qe7 8. Nc3 c6 9. Bg5 b5 10. Nxb5}\n\n"
    
    # Diagram at move 10
    latex_content += "\\textit{Position after 10. Nxb5 - Black's queenside is collapsing}\n\n"
    latex_content += "\\chessboard\n\n"
    
    # Continue the game
    latex_content += "\\mainline{10... cxb5 11. Bxb5+ Nbd7 12. O-O-O Rd8 13. Rxd7 Rxd7 "
    latex_content += "14. Rd1 Qe6 15. Bxd7+ Nxd7}\n\n"
    
    # Diagram at move 15
    latex_content += "\\textit{Position after 15...Nxd7 - The famous sacrifice coming}\n\n"
    latex_content += "\\chessboard\n\n"
    
    # Final moves
    latex_content += "\\mainline{16. Qb8+ Nxb8 17. Rd8#}\n\n"
    
    # Final position
    latex_content += "\\subsection*{Final Position - Checkmate!}\n\n"
    latex_content += "\\chessboard[boardfontsize=1.5em]\n\n"
    
    latex_content += generate_latex_postamble()
    
    print(latex_content)
    print("=" * 70 + "\n")


def show_fen_examples():
    """Display various FEN positions"""
    print("=" * 70)
    print("EXAMPLE 5: Common FEN Positions")
    print("=" * 70 + "\n")
    
    examples = [
        ("Starting Position", 
         "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
        
        ("After 1.e4 c5 (Sicilian Defense)", 
         "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"),
        
        ("Back Rank Mate Puzzle",
         "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1"),
        
        ("The Immortal Game - Critical Moment",
         "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 w - - 1 12"),
        
        ("Lucena Position (Endgame Study)",
         "1K6/1P6/8/8/8/8/r7/2k5 w - - 0 1"),
        
        ("Sicilian Dragon - Sharp Position",
         "r2q1rk1/1p1bbppp/p2p1n2/n3p3/4P3/2NP1NP1/PPB2PBP/R2Q1RK1 w - - 0 12")
    ]
    
    for name, fen in examples:
        print(f"{name}:")
        print(f"  {fen}\n")
    
    print("=" * 70 + "\n")


def show_usage_examples():
    """Show Python code examples"""
    print("=" * 70)
    print("EXAMPLE 6: Python Usage (when Tectonic is installed)")
    print("=" * 70 + "\n")
    
    print("""
from chess_generator import ChessDiagramGenerator
from pathlib import Path

# Initialize the generator
generator = ChessDiagramGenerator(verbose=True)

# Example 1: Single diagram
generator.generate_single_diagram(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    output_pdf=Path("starting_position.pdf"),
    title="Starting Position",
    caption="The initial chess setup"
)

# Example 2: Annotated game
pgn = '''[Event "World Championship"]
[White "Kasparov"]
[Black "Karpov"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0'''

generator.generate_annotated_game(
    pgn_content=pgn,
    output_pdf=Path("game.pdf"),
    diagrams_at_moves=[4],  # Show diagram after move 5
    show_final_position=True
)

# Example 3: Diagram at specific move
generator.generate_diagram_at_move(
    pgn_content=pgn,
    move_number=4,  # 0-indexed
    output_pdf=Path("position.pdf"),
    title="Critical Moment"
)
""")
    
    print("=" * 70 + "\n")


def show_batch_processing():
    """Show how to process multiple diagrams"""
    print("=" * 70)
    print("EXAMPLE 7: Batch Processing Multiple Games")
    print("=" * 70 + "\n")
    
    print("""
from chess_generator import ChessDiagramGenerator
from pathlib import Path
import glob

generator = ChessDiagramGenerator(verbose=True)

# Process all PGN files in a directory
pgn_files = glob.glob("games/*.pgn")

for pgn_file in pgn_files:
    # Read the PGN
    with open(pgn_file) as f:
        pgn_content = f.read()
    
    # Generate output filename
    output_name = Path(pgn_file).stem + ".pdf"
    output_path = Path("output") / output_name
    
    # Generate annotated game
    generator.generate_annotated_game(
        pgn_content=pgn_content,
        output_pdf=output_path,
        show_final_position=True
    )
    
    print(f"Generated: {output_path}")

# Or create a puzzle book
puzzles = [
    ("6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1", "Back Rank Mate"),
    ("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4", "Fork"),
]

for i, (fen, title) in enumerate(puzzles, 1):
    generator.generate_single_diagram(
        fen=fen,
        output_pdf=Path(f"puzzles/puzzle_{i:03d}.pdf"),
        title=f"Puzzle #{i}: {title}",
        board_size="4in"
    )
""")
    
    print("=" * 70 + "\n")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("CHESS DIAGRAM GENERATOR - Demonstration")
    print("=" * 70)
    print("\nThis demo shows the LaTeX code generated for various chess diagrams.")
    print("To compile these to PDF, you need Tectonic installed.")
    print("See README.md for setup instructions.\n")
    
    demo_single_diagram()
    demo_tactical_puzzle()
    demo_annotated_game()
    demo_complex_game_with_diagrams()
    show_fen_examples()
    show_usage_examples()
    show_batch_processing()
    
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("\n1. Install Tectonic:")
    print("   - Download binaries from: https://github.com/tectonic-typesetting/tectonic/releases")
    print("   - Or install system-wide: brew install tectonic")
    print("\n2. Install Python dependencies:")
    print("   pip install chess")
    print("\n3. Run the examples:")
    print("   python examples/all_examples.py")
    print("\n4. Check the output directory for generated PDFs")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
