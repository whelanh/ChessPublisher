# Chess Diagram Generator - Project Structure

## Complete File Tree

```
chess_diagram_app/
├── bin/                           # Tectonic binaries for distribution
│   ├── linux/
│   │   └── tectonic              # Linux binary (~50MB) - download separately
│   ├── windows/
│   │   └── tectonic.exe          # Windows binary (~50MB) - download separately
│   ├── macos/
│   │   └── tectonic              # macOS binary (~50MB) - download separately
│   └── DOWNLOAD_TECTONIC.md      # Instructions for obtaining binaries
│
├── examples/                      # Usage examples
│   ├── all_examples.py           # Complete working examples (requires Tectonic)
│   └── show_latex_examples.py    # Shows LaTeX without compilation
│
├── output/                        # Generated PDFs go here
│   └── (PDFs will be created here)
│
├── chess_generator.py             # Main application code
├── demo_latex_output.py           # Standalone demo (no Tectonic needed)
├── requirements.txt               # Python dependencies
├── setup.py                       # Package configuration
├── MANIFEST.in                    # Packaging manifest
├── .gitignore                     # Git ignore rules
├── LICENSE                        # MIT License
├── README.md                      # Full documentation
├── QUICKSTART.md                  # Quick start guide
└── PROJECT_STRUCTURE.md           # This file
```

## Core Components

### 1. chess_generator.py (Main Application)

**Classes:**
- `TectonicEngine`: Manages Tectonic LaTeX compilation
  - Auto-detects platform (Windows/Linux/macOS)
  - Finds bundled or system Tectonic
  - Compiles LaTeX to PDF
  
- `ChessDiagramGenerator`: Main API for users
  - `generate_single_diagram()`: Create diagram from FEN
  - `generate_annotated_game()`: Create full game with notation
  - `generate_diagram_at_move()`: Extract position at specific move

### 2. Binary Distribution (bin/)

The application supports bundled Tectonic binaries for distribution:
- Place platform-specific binaries in `bin/{platform}/`
- Application auto-detects and uses bundled binary
- Falls back to system Tectonic if no bundled binary found
- See `bin/DOWNLOAD_TECTONIC.md` for download instructions

### 3. Examples

**all_examples.py**: 8 complete examples showing all features
- Example 1: Basic diagram from FEN
- Example 2: Starting position
- Example 3: Tactical puzzle
- Example 4: Complete annotated game (Opera Game)
- Example 5: Scholar's Mate game
- Example 6: Diagram at specific move
- Example 7: Endgame position
- Example 8: Complex middlegame

**show_latex_examples.py**: Shows LaTeX code without compilation
- Useful for understanding what's being generated
- Works without Tectonic installed

**demo_latex_output.py**: Standalone demonstration
- Shows all LaTeX examples
- No Tectonic required
- Great for learning

## Distribution Strategies

### Strategy 1: Include Binaries (Recommended)

**Pros:**
- Users don't need to install anything
- Guaranteed consistent behavior
- Works immediately after download

**Cons:**
- Larger package size (~150MB with all 3 platforms)
- Need to update binaries when Tectonic updates

**Package Structure:**
```
your_app_v1.0.zip
├── chess_generator.py
├── bin/
│   ├── linux/tectonic
│   ├── windows/tectonic.exe
│   └── macos/tectonic
├── examples/
└── README.md
```

### Strategy 2: System Installation Required

**Pros:**
- Tiny package (~100KB)
- Always uses latest Tectonic
- Users can update Tectonic independently

**Cons:**
- Users must install Tectonic separately
- Installation varies by platform

**Instructions for users:**
```bash
# Install Tectonic first
brew install tectonic  # macOS
# or download from: https://tectonic-typesetting.github.io/

# Then install your app
pip install chess-diagram-generator
```

### Strategy 3: Hybrid (Best of Both)

Ship with binaries but support system installation:
- App tries bundled binary first
- Falls back to system Tectonic
- Users can delete bundled binaries to save space
- Already implemented in `TectonicEngine`

## Usage Patterns

### Pattern 1: Single Script

For simple use cases:
```python
from chess_generator import ChessDiagramGenerator

gen = ChessDiagramGenerator()
gen.generate_single_diagram(fen, "output.pdf")
```

### Pattern 2: Batch Processing

For processing multiple games:
```python
import glob

gen = ChessDiagramGenerator(verbose=True)

for pgn_file in glob.glob("games/*.pgn"):
    # Process each game
    ...
```

### Pattern 3: Integration in Larger App

For chess book publishers, etc.:
```python
class ChessBookPublisher:
    def __init__(self):
        self.generator = ChessDiagramGenerator()
    
    def add_chapter(self, games):
        for game in games:
            self.generator.generate_annotated_game(...)
```

## File Format Support

### Input Formats
- **FEN**: Forsyth-Edwards Notation for positions
- **PGN**: Portable Game Notation for games

### Output Format
- **PDF**: Publication-ready, vector graphics
- Scalable to any size
- Embedded fonts
- Professional typography

## Customization Points

Users can customize by modifying:

1. **Board Styling** (in `_generate_latex_preamble()`):
   ```latex
   \setchessboard{
       showmover=true,
       pgfstyle=color,
       boardfontsize=2em
   }
   ```

2. **Page Layout**:
   ```latex
   \usepackage[margin=0.5in]{geometry}
   ```

3. **Piece Sets**: Supported by xskak package
   - Default, alpha, modern, etc.

## Testing

To verify installation:
```bash
# 1. Test LaTeX generation (no Tectonic needed)
python demo_latex_output.py

# 2. Test actual PDF generation (requires Tectonic)
python examples/all_examples.py

# 3. Check output
ls output/
```

## Platform-Specific Notes

### Windows
- Binary: `tectonic.exe`
- Platform string: `'win32'`
- Path separator: `\`

### Linux  
- Binary: `tectonic`
- Platform string: `'linux'`
- Path separator: `/`
- Make executable: `chmod +x bin/linux/tectonic`

### macOS
- Binary: `tectonic`
- Platform string: `'darwin'`
- Path separator: `/`
- Two architectures: Intel (x86_64), Apple Silicon (aarch64)
- Make executable: `chmod +x bin/macos/tectonic`

## Dependencies

### Required
- Python 3.7+
- python-chess (for PGN/FEN handling)
- Tectonic (bundled or system)

### Optional
- setuptools (for packaging)
- pytest (for testing)

## Performance

Typical compilation times:
- Single diagram: 2-5 seconds
- Annotated game: 3-7 seconds
- Batch (100 diagrams): 5-10 minutes

## Size Estimates

- Source code: ~30 KB
- Tectonic binary (one platform): ~50 MB
- Generated PDF (single diagram): ~20 KB
- Generated PDF (full game): ~30-50 KB

## Future Enhancements

Potential additions:
- SVG output option
- PNG export (via pdf2image)
- Custom piece sets
- Board rotation
- Multiple languages
- Theme support
- Command-line interface
- GUI application

## Support & Resources

- Tectonic docs: https://tectonic-typesetting.github.io/
- xskak package: https://ctan.org/pkg/xskak
- python-chess: https://python-chess.readthedocs.io/
- PGN format: https://en.wikipedia.org/wiki/Portable_Game_Notation
- FEN format: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
