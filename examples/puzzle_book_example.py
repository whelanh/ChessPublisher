"""
Real-World Example: Creating a Chess Puzzle Book

This example demonstrates how to use the Chess Diagram Generator
to create a complete puzzle book with multiple diagrams.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from chess_generator import ChessDiagramGenerator


class PuzzleBook:
    """Generate a chess puzzle book"""
    
    def __init__(self, title="Chess Tactics", output_dir="puzzle_book"):
        self.title = title
        self.generator = ChessDiagramGenerator(verbose=True)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Track puzzles for a table of contents
        self.puzzles = []
    
    def add_puzzle(self, fen, title, difficulty, solution_hint=None):
        """Add a puzzle to the book"""
        puzzle_num = len(self.puzzles) + 1
        filename = f"puzzle_{puzzle_num:03d}_{difficulty.lower()}.pdf"
        
        caption = f"Difficulty: {difficulty}"
        if solution_hint:
            caption += f" | Hint: {solution_hint}"
        
        success = self.generator.generate_single_diagram(
            fen=fen,
            output_pdf=self.output_dir / filename,
            title=f"Puzzle #{puzzle_num}: {title}",
            caption=caption,
            board_size="4in"
        )
        
        if success:
            self.puzzles.append({
                'number': puzzle_num,
                'title': title,
                'difficulty': difficulty,
                'filename': filename
            })
            print(f"✓ Added puzzle {puzzle_num}")
        
        return success
    
    def generate_table_of_contents(self):
        """Create a TOC file"""
        toc_file = self.output_dir / "TABLE_OF_CONTENTS.txt"
        
        with open(toc_file, 'w') as f:
            f.write(f"{self.title}\n")
            f.write("=" * len(self.title) + "\n\n")
            
            # Group by difficulty
            difficulties = {}
            for puzzle in self.puzzles:
                diff = puzzle['difficulty']
                if diff not in difficulties:
                    difficulties[diff] = []
                difficulties[diff].append(puzzle)
            
            for diff in ['Beginner', 'Intermediate', 'Advanced', 'Expert']:
                if diff in difficulties:
                    f.write(f"\n{diff}\n")
                    f.write("-" * len(diff) + "\n")
                    for p in difficulties[diff]:
                        f.write(f"  {p['number']:3d}. {p['title']} ({p['filename']})\n")
        
        print(f"\n✓ Generated table of contents: {toc_file}")
    
    def print_summary(self):
        """Print summary statistics"""
        print(f"\nPuzzle Book Summary")
        print("=" * 50)
        print(f"Title: {self.title}")
        print(f"Total Puzzles: {len(self.puzzles)}")
        print(f"Output Directory: {self.output_dir}")
        
        # Count by difficulty
        from collections import Counter
        difficulties = Counter(p['difficulty'] for p in self.puzzles)
        print("\nBy Difficulty:")
        for diff, count in sorted(difficulties.items()):
            print(f"  {diff}: {count}")
        print("=" * 50)


def create_sample_puzzle_book():
    """Create a sample puzzle book with various tactics"""
    
    print("=" * 70)
    print("Creating Sample Chess Puzzle Book")
    print("=" * 70 + "\n")
    
    book = PuzzleBook("Tactical Mastery: 20 Essential Puzzles")
    
    # Beginner puzzles
    puzzles_beginner = [
        {
            'fen': "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1",
            'title': "Back Rank Mate",
            'difficulty': "Beginner",
            'hint': "The rook is powerful on the 8th rank"
        },
        {
            'fen': "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
            'title': "Scholar's Mate Pattern",
            'difficulty': "Beginner",
            'hint': "Queen and bishop work together"
        },
        {
            'fen': "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
            'title': "Fork the King and Rook",
            'difficulty': "Beginner",
            'hint': "Knights can fork"
        },
    ]
    
    # Intermediate puzzles
    puzzles_intermediate = [
        {
            'fen': "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 4 5",
            'title': "Fried Liver Attack",
            'difficulty': "Intermediate",
            'hint': "Sacrifice to expose the king"
        },
        {
            'fen': "r1bqkb1r/pppp1ppp/5n2/4p3/2BnP3/5N2/PPPP1PPP/RNBQ1RK1 b kq - 5 5",
            'title': "Knight Fork on f2",
            'difficulty': "Intermediate",
            'hint': "A royal fork is possible"
        },
        {
            'fen': "2kr3r/ppp2ppp/2n5/3Np3/2P5/8/PP3PPP/R4RK1 w - - 0 15",
            'title': "Discovered Attack",
            'difficulty': "Intermediate",
            'hint': "Moving one piece reveals another"
        },
    ]
    
    # Advanced puzzles
    puzzles_advanced = [
        {
            'fen': "r1bqk2r/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPP2PPP/R1BQK2R w KQkq - 4 6",
            'title': "Greco Sacrifice",
            'difficulty': "Advanced",
            'hint': "A classic bishop sacrifice on h7"
        },
        {
            'fen': "r1b2rk1/ppp2ppp/2n5/3q4/3P4/2PB4/PP3PPP/R2Q1RK1 w - - 0 12",
            'title': "Smothered Mate Pattern",
            'difficulty': "Advanced",
            'hint': "The king's own pieces trap it"
        },
    ]
    
    # Expert puzzles
    puzzles_expert = [
        {
            'fen': "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 w - - 1 12",
            'title': "Immortal Game Position",
            'difficulty': "Expert",
            'hint': "Both rooks were sacrificed!"
        },
        {
            'fen': "1r4k1/7p/5np1/3p4/8/2N5/1P4PP/6K1 w - - 0 30",
            'title': "Endgame Breakthrough",
            'difficulty': "Expert",
            'hint': "Create a passed pawn"
        },
    ]
    
    # Add all puzzles to the book
    all_puzzles = puzzles_beginner + puzzles_intermediate + puzzles_advanced + puzzles_expert
    
    for puzzle in all_puzzles:
        book.add_puzzle(**puzzle)
    
    # Generate table of contents
    book.generate_table_of_contents()
    
    # Print summary
    book.print_summary()
    
    print("\n" + "=" * 70)
    print(f"Puzzle book created in: {book.output_dir}/")
    print("=" * 70 + "\n")


def create_opening_repertoire():
    """Example: Create an opening repertoire with annotated games"""
    
    print("\n" + "=" * 70)
    print("Creating Opening Repertoire")
    print("=" * 70 + "\n")
    
    generator = ChessDiagramGenerator(verbose=True)
    output_dir = Path("opening_repertoire")
    output_dir.mkdir(exist_ok=True)
    
    # Sample games for different openings
    games = {
        "Italian_Game": """[Event "Italian Game Model"]
[White "Student"]
[Black "Opponent"]
[Result "*"]

1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. c3 Nf6 5. d4 exd4 6. cxd4 Bb4+ 7. Nc3 *""",
        
        "Sicilian_Dragon": """[Event "Sicilian Dragon"]
[White "Player"]
[Black "Opponent"]
[Result "*"]

1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 g6 6. Be3 Bg7 7. f3 O-O *""",
    }
    
    for opening_name, pgn in games.items():
        output_file = output_dir / f"{opening_name}.pdf"
        generator.generate_annotated_game(
            pgn_content=pgn,
            output_pdf=output_file,
            show_final_position=True
        )
    
    print(f"\n✓ Opening repertoire created in: {output_dir}/")


def main():
    """Run all examples"""
    
    print("\n" + "=" * 70)
    print("REAL-WORLD EXAMPLE: Chess Puzzle Book Generator")
    print("=" * 70)
    print("\nThis example demonstrates creating a complete puzzle book")
    print("with multiple difficulty levels and various tactical themes.\n")
    
    try:
        # Create puzzle book
        create_sample_puzzle_book()
        
        # Create opening repertoire
        create_opening_repertoire()
        
        print("\n" + "=" * 70)
        print("SUCCESS! All examples completed.")
        print("=" * 70)
        print("\nGenerated directories:")
        print("  - puzzle_book/        (20 tactical puzzles)")
        print("  - opening_repertoire/ (annotated opening games)")
        print("\n" + "=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. Tectonic is installed (see bin/DOWNLOAD_TECTONIC.md)")
        print("  2. python-chess is installed (pip install chess)")


if __name__ == "__main__":
    main()
