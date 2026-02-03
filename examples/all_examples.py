"""
Complete examples demonstrating all features of the Chess Diagram Generator
"""

from pathlib import Path
import sys

# Add parent directory to path to import chess_generator
sys.path.insert(0, str(Path(__file__).parent.parent))

from chess_generator import ChessDiagramGenerator


def example_1_basic_diagram():
    """Example 1: Generate a single diagram from FEN"""
    print("\n=== Example 1: Basic Diagram from FEN ===")
    
    generator = ChessDiagramGenerator(verbose=True)
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # The Immortal Game position after 11...Nxf3+
    fen = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 w - - 1 12"
    
    success = generator.generate_single_diagram(
        fen=fen,
        output_pdf=output_dir / "example1_immortal_game.pdf",
        title="The Immortal Game",
        caption="Position after 11...Nxf3+ - White sacrificed both rooks!",
        board_size="4in"
    )
    
    if success:
        print("✓ Generated: example1_immortal_game.pdf")
    else:
        print("✗ Failed to generate diagram")


def example_2_starting_position():
    """Example 2: Standard starting position"""
    print("\n=== Example 2: Starting Position ===")
    
    generator = ChessDiagramGenerator(verbose=True)
    output_dir = Path(__file__).parent.parent / "output"
    
    # Standard starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    success = generator.generate_single_diagram(
        fen=fen,
        output_pdf=output_dir / "example2_starting_position.pdf",
        title="Chess Starting Position",
        caption="The initial setup for a game of chess"
    )
    
    if success:
        print("✓ Generated: example2_starting_position.pdf")


def example_3_tactical_puzzle():
    """Example 3: A tactical puzzle"""
    print("\n=== Example 3: Tactical Puzzle ===")
    
    generator = ChessDiagramGenerator(verbose=True)
    output_dir = Path(__file__).parent.parent / "output"
    
    # White to move and win
    fen = "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1"
    
    success = generator.generate_single_diagram(
        fen=fen,
        output_pdf=output_dir / "example3_back_rank_mate.pdf",
        title="Puzzle: White to Move and Win",
        caption="Find the back rank mate in 1 move!",
        board_size="3.5in"
    )
    
    if success:
        print("✓ Generated: example3_back_rank_mate.pdf")


def example_4_annotated_game():
    """Example 4: Complete annotated game with diagrams"""
    print("\n=== Example 4: Annotated Game ===")
    
    generator = ChessDiagramGenerator(verbose=True)
    output_dir = Path(__file__).parent.parent / "output"
    
    # The Opera Game: Morphy vs Duke of Brunswick and Count Isouard (1858)
    pgn = """[Event "Opera Game"]
[Site "Paris"]
[Date "1858.??.??"]
[White "Paul Morphy"]
[Black "Duke of Brunswick and Count Isouard"]
[Result "1-0"]

1. e4 e5 2. Nf3 d6 3. d4 Bg4 4. dxe5 Bxf3 5. Qxf3 dxe5 6. Bc4 Nf6 7. Qb3 Qe7 
8. Nc3 c6 9. Bg5 b5 10. Nxb5 cxb5 11. Bxb5+ Nbd7 12. O-O-O Rd8 13. Rxd7 Rxd7 
14. Rd1 Qe6 15. Bxd7+ Nxd7 16. Qb8+ Nxb8 17. Rd8# 1-0"""
    
    # Show diagrams at key moments
    success = generator.generate_annotated_game(
        pgn_content=pgn,
        output_pdf=output_dir / "example4_opera_game.pdf",
        diagrams_at_moves=[10, 15],  # Show position after moves 11 and 16
        show_final_position=True
    )
    
    if success:
        print("✓ Generated: example4_opera_game.pdf")


def example_5_scholars_mate():
    """Example 5: Scholar's Mate"""
    print("\n=== Example 5: Scholar's Mate Game ===")
    
    generator = ChessDiagramGenerator(verbose=True)
    output_dir = Path(__file__).parent.parent / "output"
    
    pgn = """[Event "Scholar's Mate Example"]
[Site "Teaching Game"]
[Date "2024.??.??"]
[White "Student"]
[Black "Beginner"]
[Result "1-0"]

1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7# 1-0"""
    
    success = generator.generate_annotated_game(
        pgn_content=pgn,
        output_pdf=output_dir / "example5_scholars_mate.pdf",
        show_final_position=True
    )
    
    if success:
        print("✓ Generated: example5_scholars_mate.pdf")


def example_6_diagram_at_specific_move():
    """Example 6: Extract diagram at a specific move number"""
    print("\n=== Example 6: Diagram at Specific Move ===")
    
    generator = ChessDiagramGenerator(verbose=True)
    output_dir = Path(__file__).parent.parent / "output"
    
    # Game leading to Scholar's Mate
    pgn = """[Event "Teaching"]
[White "White"]
[Black "Black"]
[Result "1-0"]

1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7# 1-0"""
    
    # Show position after move 6 (after 3. Qh5)
    success = generator.generate_diagram_at_move(
        pgn_content=pgn,
        move_number=5,  # 0-indexed: move 6 is index 5
        output_pdf=output_dir / "example6_position_after_qh5.pdf",
        title="Critical Moment: After 3. Qh5"
    )
    
    if success:
        print("✓ Generated: example6_position_after_qh5.pdf")


def example_7_endgame_position():
    """Example 7: Lucena Position (endgame study)"""
    print("\n=== Example 7: Endgame Study ===")
    
    generator = ChessDiagramGenerator(verbose=True)
    output_dir = Path(__file__).parent.parent / "output"
    
    # The Lucena Position
    fen = "1K6/1P6/8/8/8/8/r7/2k5 w - - 0 1"
    
    success = generator.generate_single_diagram(
        fen=fen,
        output_pdf=output_dir / "example7_lucena_position.pdf",
        title="The Lucena Position",
        caption="A fundamental winning position in rook endgames",
        board_size="3.5in"
    )
    
    if success:
        print("✓ Generated: example7_lucena_position.pdf")


def example_8_complex_middle_game():
    """Example 8: Complex middlegame position"""
    print("\n=== Example 8: Complex Middlegame ===")
    
    generator = ChessDiagramGenerator(verbose=True)
    output_dir = Path(__file__).parent.parent / "output"
    
    # Sicilian Defense - Dragon Variation
    fen = "r2q1rk1/1p1bbppp/p2p1n2/n3p3/4P3/2NP1NP1/PPB2PBP/R2Q1RK1 w - - 0 12"
    
    success = generator.generate_single_diagram(
        fen=fen,
        output_pdf=output_dir / "example8_sicilian_dragon.pdf",
        title="Sicilian Defense - Dragon Variation",
        caption="Sharp theoretical position with opposite-side castling",
        board_size="4in"
    )
    
    if success:
        print("✓ Generated: example8_sicilian_dragon.pdf")


def run_all_examples():
    """Run all examples"""
    print("=" * 60)
    print("Chess Diagram Generator - Complete Examples")
    print("=" * 60)
    
    examples = [
        example_1_basic_diagram,
        example_2_starting_position,
        example_3_tactical_puzzle,
        example_4_annotated_game,
        example_5_scholars_mate,
        example_6_diagram_at_specific_move,
        example_7_endgame_position,
        example_8_complex_middle_game
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"✗ Error in {example.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("Check the 'output' directory for generated PDFs")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()
