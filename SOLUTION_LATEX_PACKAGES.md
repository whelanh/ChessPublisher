# Solution: Bundling LaTeX Packages for Cross-Platform Use

## Problem Summary

The chess diagram generator was designed to use **Tectonic** as a portable, self-contained LaTeX engine alternative. However, **Tectonic does NOT include chess-related LaTeX packages** (`xskak`, `chessboard`, `skak`, `chessfss`) in its default bundle, and it cannot download them on-demand from CTAN.

This creates a critical dependency issue that breaks the "portable" promise of the project.

## Solutions (In Order of Recommendation)

### Solution 1: Bundle LaTeX Package Files (Current Approach - 90% Complete)

**Status:** In progress - missing only chessfss.sty and associated font files

**What I've done:**
1. Downloaded and built the following packages:
   - `xskak` (xskak.sty, xskak-keys.sty, xskak-nagdef.sty)
   - `chessboard` (chessboard.sty, chessboard-pgf.sty, chessboard-keys-main.sty, chessboard-keys-pgf.sty)
   - `skak` (skak.sty)

2. Modified `chess_generator.py` to copy these bundled .sty files to the compilation directory

3. Stored all .sty files in `latex_sty/` directory

**What's still needed:**
- `chessfss.sty` and associated font definition files (.fd files)
- Font files themselves (chess piece fonts)

**To complete this solution:**

```bash
# You need to manually obtain chessfss from TeX Live or CTAN
# Option A: If you have access to any system with TeX Live:
find /usr/share/texlive -name "chessfss*" -o -name "*chess*.fd"

# Copy those files to latex_sty/

# Option B: Download from working CTAN mirror or TeX Live ISO
# The package includes:
# - chessfss.sty
# - ufigchess.fd, ulschess.fd, usgchess.fd, etc. (font definitions)
# - Chess fonts in various formats
```

### Solution 2: Switch to pdflatex/xelatex (Recommended for Most Users)

**Pros:**
- Works immediately on any system with TeX Live installed
- All packages available through package managers
- More reliable, better tested
- Still cross-platform

**Cons:**
- Requires ~2-5GB TeX Live installation
- Not as "portable" as Tectonic was supposed to be

**Implementation:**

Modify `TectonicEngine` class in `chess_generator.py` to detect and use pdflatex if available:

```python
class LaTeXEngine:
    """Manages LaTeX compilation - supports both Tectonic and pdflatex"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.engine_type, self.engine_path = self._find_latex_engine()
        
        if not self.engine_path:
            raise RuntimeError(
                "No LaTeX engine found. Please install either:\\n"
                "1. TeX Live (includes pdflatex): Fedora: texlive-scheme-basic\\n"
                "2. Tectonic (lightweight): brew install tectonic\\n"
            )
    
    def _find_latex_engine(self) -> Tuple[str, Optional[Path]]:
        """Find available LaTeX engine"""
        # Try pdflatex first (more reliable for chess packages)
        pdflatex = shutil.which('pdflatex')
        if pdflatex:
            return ('pdflatex', Path(pdflatex))
        
        # Try xelatex
        xelatex = shutil.which('xelatex')
        if xelatex:
            return ('xelatex', Path(xelatex))
        
        # Fall back to Tectonic
        tectonic = shutil.which('tectonic')
        if tectonic:
            return ('tectonic', Path(tectonic))
        
        # Try bundled Tectonic
        # ... existing bundled binary logic ...
        
        return (None, None)
```

### Solution 3: Use Flatpak/Container with TeX Live

For immutable systems like yours, package the application with TeX Live in a container:

```dockerfile
# Dockerfile
FROM fedora:latest

RUN dnf install -y texlive-scheme-basic texlive-xskak texlive-chessboard python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
```

Or create a Flatpak manifest that includes TeX Live.

### Solution 4: Download Packages On First Run

Create a setup script that downloads the necessary .sty and font files on first run:

```python
def setup_latex_packages():
    """Download and cache LaTeX packages on first run"""
    cache_dir = Path.home() / '.chess_diagram_generator' / 'latex_packages'
    
    if not cache_dir.exists():
        print("First-time setup: Downloading LaTeX packages...")
        # Download xskak, chessboard, skak, chessfss from CTAN
        # Extract and cache them
        cache_dir.mkdir(parents=True)
        # ... download logic ...
```

## Immediate Fix for Your System

Since you're on an immutable Fedora system, your best options are:

### Option A: Use Toolbox/Distrobox (Recommended)

```bash
# Create a development container with TeX Live
toolbox create chess-dev
toolbox enter chess-dev

# Inside the container:
sudo dnf install texlive-scheme-basic texlive-xskak texlive-chessboard
pip install chess

# Run the examples
cd /var/home/hugh/Downloads/chess_diagram_app
python3 examples/all_examples.py
```

### Option B: Flatpak TeX Live

```bash
# Install TeX Live via Flatpak
flatpak install flathub org.texstudio.TeXstudio  # Includes TeX Live

# Then modify chess_generator.py to use the Flatpak's pdflatex
```

### Option C: Complete the Bundled Solution

I need the chessfss package files. Can you:

1. Access any computer with TeX Live installed?
2. Run: `find /usr/share/texlive -path "*/tex/latex/chessfss/*"`
3. Copy those files to the project's `latex_sty/` directory

## Updated Documentation

I've created:
- `verify_setup.py` - Diagnoses setup issues
- `TROUBLESHOOTING.md` - Comprehensive troubleshooting guide
- Updated README.md with setup instructions

## Recommendation

**For your project:** I recommend **Solution 2** (supporting pdflatex/xelatex) as the primary method, with Tectonic as an optional lightweight alternative.

**For immediate use:** Use **toolbox/distrobox** with TeX Live installed.

The "portable Tectonic" approach is fundamentally broken for chess diagrams due to missing packages in Tectonic's bundle. This is a known limitation of Tectonic - it only includes a subset of CTAN packages.

## Next Steps

Would you like me to:
1. Implement Solution 2 (add pdflatex/xelatex support)?
2. Help you set up a toolbox environment?
3. Try to locate and download the remaining chessfss files?
4. Create a Flatpak/container solution?
