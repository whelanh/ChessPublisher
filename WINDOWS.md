# Windows Usage Guide

This guide addresses Windows-specific considerations for using ChessPublisher.

## Known Issues and Solutions

### Path Issues with Temp Directories

**Problem**: On Windows, usernames with long directory names (e.g., `C:\Users\MyName\...`) are sometimes converted to short 8.3 format paths (e.g., `C:\Users\MYNAME~1\...`). The tilde (`~`) in these paths can cause LaTeX engines like pdflatex to fail with errors like:

```
! I can't find file `C:/Users/MYNAME'.
```

**Solution**: ChessPublisher automatically converts short 8.3 paths to long paths before passing them to the LaTeX engine. This fix is built into the library.

If you still encounter path issues, you can use a custom working directory in a simple path:

```python
from pathlib import Path
from chess_generator import ChessDiagramGenerator

generator = ChessDiagramGenerator(verbose=True)

# Use a simple path without spaces or special characters
working_dir = Path("C:/chess/temp")
working_dir.mkdir(parents=True, exist_ok=True)
```

## Generating LaTeX Files Only (tex_only mode)

If you want to inspect, modify, or compile the LaTeX code yourself, you can use the `tex_only=True` parameter:

```python
from pathlib import Path
from chess_generator import ChessDiagramGenerator

generator = ChessDiagramGenerator(verbose=True)

# Generate only the .tex file, without compiling to PDF
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
generator.generate_single_diagram(
    fen=fen,
    output_path=Path("output/starting_position.pdf"),  # Will save as .tex
    title="Starting Position",
    tex_only=True  # Saves .tex file instead of compiling to PDF
)
```

This works with all generation methods:
- `generate_single_diagram(..., tex_only=True)`
- `generate_diagram_at_move(..., tex_only=True)`
- `generate_annotated_game(..., tex_only=True)`

The `.tex` file will be saved in the same location as the intended PDF output, with the extension changed to `.tex`.

## Using LuaLaTeX

If you prefer LuaLaTeX over pdfLaTeX (e.g., for better OpenType font support), you can specify it as your preferred engine:

```python
from chess_generator import ChessDiagramGenerator

# Use LuaLaTeX instead of pdfLaTeX
generator = ChessDiagramGenerator(
    verbose=True,
    preferred_engine='lualatex'
)

# Now all compilations will use LuaLaTeX
generator.generate_single_diagram(...)
```

### Supported Engines

The following LaTeX engines are supported (in default priority order):
1. **pdflatex** - Most reliable for chess packages
2. **lualatex** - Better OpenType font support, modern features
3. **xelatex** - Good Unicode and font support
4. **tectonic** - Modern, self-contained engine (limited chess package support)

### LuaLaTeX Advantages

- Direct use of system fonts (OpenType, TrueType)
- No need for MAP files or font encoding issues
- Modern Lua scripting capabilities
- Better handling of Unicode text

### Note on Font Configuration

When using LuaLaTeX, you generally don't need to configure MAP files for fonts. If you encounter font issues with pdfLaTeX, switching to LuaLaTeX often resolves them:

```python
# If pdflatex has font issues, try lualatex
generator = ChessDiagramGenerator(preferred_engine='lualatex')
```

## TeX Live on Windows

If you're using TeX Live on Windows, make sure your PATH includes the TeX Live bin directory (e.g., `C:\texlive\2024\bin\windows`).

Install required chess packages if not already present:

```cmd
tlmgr install xskak chessboard chessfss skak
```

## Troubleshooting

### "I can't find file" errors

1. Check if the path contains tildes (`~`) - the automatic fix should handle this
2. Try moving your project to a simpler path (e.g., `C:\chess\project`)
3. Use `tex_only=True` to generate the `.tex` file, then compile manually

### Font/MAP file errors

1. Try using LuaLaTeX: `ChessDiagramGenerator(preferred_engine='lualatex')`
2. Update your TeX distribution: `tlmgr update --all`
3. Regenerate font maps: `mktexlsr` and `updmap-sys`

### Permission errors

1. Don't run from system-protected directories
2. Ensure you have write access to the output directory
3. Close any PDF viewers that might have the output file open
