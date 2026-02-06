# Windows VM Setup and Testing Guide

This guide walks you through setting up a fresh Windows machine to test ChessPublisher.

## Step 1: Install Python

1. Download Python from https://www.python.org/downloads/windows/
2. Run the installer
3. **IMPORTANT**: Check ✅ "Add Python to PATH" at the bottom of the installer
4. Click "Install Now"

Verify installation by opening Command Prompt (Win+R, type `cmd`, press Enter):
```cmd
python --version
```

## Step 2: Install TeX Live

TeX Live is recommended for Windows. MiKTeX is an alternative.

### Option A: TeX Live (Recommended)

1. Download the installer from https://tug.org/texlive/acquire-netinstall.html
   - Click "install-tl-windows.exe"
2. Run the installer
3. Choose "Install" (full installation takes ~5GB and 30-60 minutes)
   - For a smaller install, click "Advanced" and select "basic" scheme
4. Wait for installation to complete

After installation, open a **new** Command Prompt and verify:
```cmd
pdflatex --version
```

### Option B: MiKTeX (Alternative)

1. Download from https://miktex.org/download
2. Run the installer
3. Choose "Install missing packages on-the-fly: Yes"
4. Complete installation

## Step 3: Install LaTeX Chess Packages

Open Command Prompt **as Administrator** (right-click → Run as administrator):

For TeX Live:
```cmd
tlmgr install xskak chessboard chessfss skak
```

For MiKTeX, packages install automatically on first use, but you can pre-install:
```cmd
mpm --install=xskak
mpm --install=chessboard
mpm --install=chessfss
mpm --install=skak
```

## Step 4: Get ChessPublisher

### Option A: Clone with Git
If you have Git installed:
```cmd
git clone https://github.com/YOUR_USERNAME/chessPublisher.git
cd chessPublisher
git checkout windows_issues
```

### Option B: Copy from shared folder
If you have a shared folder with your Linux host, copy the entire `chessPublisher` folder to your Windows VM (e.g., to `C:\chess\chessPublisher`).

### Option C: Download ZIP
Download the repository as a ZIP file and extract it.

## Step 5: Install Python Dependencies

Open Command Prompt and navigate to the project:
```cmd
cd C:\path\to\chessPublisher
pip install -r requirements.txt
```

This installs the `chess` library for PGN parsing.

## Step 6: Run Tests

### Test 1: Basic Syntax Check
```cmd
python -m py_compile chess_generator.py
```
No output means success.

### Test 2: Run All Examples
```cmd
python examples/all_examples.py
```

This should generate 8 PDF files in the `output/` directory.

### Test 3: Test tex_only Mode
```cmd
python -c "from pathlib import Path; from chess_generator import ChessDiagramGenerator; g = ChessDiagramGenerator(verbose=True); g.generate_single_diagram('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', Path('output/test.pdf'), title='Test', tex_only=True)"
```

Check that `output/test.tex` was created.

### Test 4: Test LuaLaTeX (if installed)
```cmd
python -c "from chess_generator import ChessDiagramGenerator; g = ChessDiagramGenerator(verbose=True, preferred_engine='lualatex'); print('Engine:', g.engine.engine_type)"
```

## Expected Results

✅ All examples should complete without "I can't find file" errors
✅ PDF files should be generated in the `output/` folder
✅ The `tex_only=True` option should create `.tex` files instead of PDFs

## Troubleshooting

### "python is not recognized"
- Reinstall Python and make sure to check "Add Python to PATH"
- Or manually add Python to PATH: Search "Environment Variables" → Edit PATH → Add Python install directory

### "pdflatex is not recognized"
- TeX Live may not be in PATH. Add `C:\texlive\2024\bin\windows` to your PATH
- Or restart Command Prompt after TeX Live installation

### "I can't find file" errors with paths containing ~
- This should be fixed automatically now
- If it persists, try moving the project to a simple path like `C:\chess\chessPublisher`

### Package not found errors
- Run `tlmgr install xskak chessboard chessfss skak` again
- For MiKTeX, run MiKTeX Console → Updates → Check for updates

### Permission errors
- Don't run from `C:\Program Files` or other protected directories
- Use a folder like `C:\chess\` or your Documents folder

## Quick Test Script

Save this as `test_windows.py` in the chessPublisher directory:

```python
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
```

Run it with:
```cmd
python test_windows.py
```
