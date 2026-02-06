"""Quick Windows compatibility test"""
from pathlib import Path
from chess_generator import ChessDiagramGenerator

print("=" * 50)
print("ChessPublisher Windows Test")
print("=" * 50)

# Test 1: Basic diagram
print("\n1. Testing basic diagram generation...")
g = ChessDiagramGenerator(verbose=True)
success = g.generate_single_diagram(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    output_path=Path("output/windows_test.pdf"),
    title="Windows Test"
)
print(f"   Result: {'PASS' if success else 'FAIL'}")

# Test 2: tex_only mode
print("\n2. Testing tex_only mode...")
success = g.generate_single_diagram(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    output_path=Path("output/windows_test_texonly.pdf"),
    title="TeX Only Test",
    tex_only=True
)
tex_exists = Path("output/windows_test_texonly.tex").exists()
print(f"   Result: {'PASS' if success and tex_exists else 'FAIL'}")

# Test 3: Annotated game
print("\n3. Testing annotated game...")
pgn = '''[Event "Test"]
[White "White"]
[Black "Black"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 1-0'''

success = g.generate_annotated_game(
    pgn_content=pgn,
    output_path=Path("output/windows_test_game.pdf")
)
print(f"   Result: {'PASS' if success else 'FAIL'}")

print("\n" + "=" * 50)
print("Tests complete! Check the output/ folder for generated files.")
print("=" * 50)
