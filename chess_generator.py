"""
Chess Diagram Generator
A cross-platform tool for generating publication-ready chess diagrams and annotated games.
Uses Tectonic LaTeX engine for high-quality output.
"""

import subprocess
import sys
import shutil
from pathlib import Path
from typing import Optional, List, Tuple
import tempfile
import os


class LaTeXEngine:
    """Manages LaTeX compilation across platforms - supports pdflatex, xelatex, and Tectonic"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.engine_type, self.engine_path = self._find_latex_engine()
        
        if not self.engine_path:
            raise RuntimeError(
                "No LaTeX engine found. Please install one of:\n"
                "1. TinyTeX (recommended): wget -qO- https://yihui.org/tinytex/install-bin-unix.sh | sh\n"
                "   Then: tlmgr install xskak chessboard chessfss skak\n"
                "2. TeX Live: Install via package manager (texlive-scheme-basic + chess packages)\n"
                "3. Tectonic: brew install tectonic (limited support, missing some packages)\n"
            )
        
        if self.verbose:
            print(f"Using {self.engine_type} at: {self.engine_path}")
    
    def _get_platform_name(self) -> str:
        """Determine the platform-specific directory name"""
        if sys.platform == 'win32':
            return 'windows'
        elif sys.platform == 'darwin':
            return 'macos'
        else:
            return 'linux'
    
    def _find_latex_engine(self) -> Tuple[str, Optional[Path]]:
        """Find available LaTeX engine - tries pdflatex, xelatex, then Tectonic"""
        # Try pdflatex first (most reliable for chess packages)
        pdflatex = shutil.which('pdflatex')
        if pdflatex:
            return ('pdflatex', Path(pdflatex))
        
        # Try xelatex
        xelatex = shutil.which('xelatex')
        if xelatex:
            return ('xelatex', Path(xelatex))
        
        # Try system Tectonic
        tectonic = shutil.which('tectonic')
        if tectonic:
            return ('tectonic', Path(tectonic))
        
        # Try bundled Tectonic binary
        base_dir = Path(__file__).parent
        platform = self._get_platform_name()
        bundled_path = base_dir / 'bin' / platform / ('tectonic.exe' if platform == 'windows' else 'tectonic')
        
        if bundled_path.exists() and bundled_path.is_file():
            return ('tectonic', bundled_path)
        
        return (None, None)
    
    def _copy_bundled_packages(self, working_dir: Path) -> None:
        """
        Copy bundled LaTeX packages to working directory.
        Only needed for Tectonic which doesn't have chess packages.
        """
        # Only copy for Tectonic - pdflatex/xelatex have packages via tlmgr
        if self.engine_type != 'tectonic':
            return
        
        base_dir = Path(__file__).parent
        sty_dir = base_dir / 'latex_sty'
        
        if sty_dir.exists():
            for sty_file in sty_dir.glob('*.sty'):
                shutil.copy2(sty_file, working_dir)
            if self.verbose:
                print(f"  Copied {len(list(sty_dir.glob('*.sty')))} bundled LaTeX packages")
    
    def compile(self, tex_content: str, output_pdf: Path, working_dir: Optional[Path] = None) -> bool:
        """
        Compile LaTeX content to PDF
        
        Args:
            tex_content: LaTeX source code as string
            output_pdf: Path where PDF should be saved
            working_dir: Directory to compile in (default: temp directory)
        
        Returns:
            True if compilation succeeded, False otherwise
        """
        if working_dir is None:
            working_dir = Path(tempfile.mkdtemp())
            cleanup = True
        else:
            working_dir = Path(working_dir)
            cleanup = False
        
        working_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy bundled LaTeX packages
        self._copy_bundled_packages(working_dir)
        
        tex_file = working_dir / 'document.tex'
        
        try:
            # Write LaTeX content
            tex_file.write_text(tex_content, encoding='utf-8')
            
            # Compile with appropriate engine
            if self.engine_type in ('pdflatex', 'xelatex'):
                # Use traditional LaTeX engines
                result = subprocess.run(
                    [str(self.engine_path), '-interaction=nonstopmode',
                     '-halt-on-error',
                     '-output-directory', str(working_dir), str(tex_file)],
                    cwd=working_dir,
                    capture_output=True,
                    text=True,
                    timeout=30  # 30 second timeout
                )
            else:
                # Use Tectonic
                result = subprocess.run(
                    [str(self.engine_path), '-X', 'compile', str(tex_file)],
                    cwd=working_dir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            if result.returncode != 0:
                # Check both stdout and stderr for errors (pdflatex uses stdout)
                error_output = result.stderr + result.stdout
                
                if self.verbose:
                    print(f"Compilation failed:")
                    if result.stderr:
                        print(f"STDERR: {result.stderr}")
                    if result.stdout:
                        print(f"STDOUT: {result.stdout[-1000:]}"  )  # Last 1000 chars
                
                # Provide helpful error messages for common issues
                if 'xskak.sty' in error_output or 'chessboard.sty' in error_output:
                    print("\n⚠️  LaTeX Package Error Detected")
                    print("The required chess packages (xskak, chessboard) are not available.")
                    print("\nSolution:")
                    if self.engine_type in ('pdflatex', 'xelatex'):
                        print("  Install packages: tlmgr install xskak chessboard chessfss skak")
                    else:
                        print("  1. Ensure you have an internet connection")
                        print("  2. Run: python3 verify_setup.py")
                        print("  3. Wait for packages to download (~30-60 seconds)")
                    print("\nFor more help, see TROUBLESHOOTING.md")
                
                return False
            
            # Move PDF to output location
            pdf_source = working_dir / 'document.pdf'
            if pdf_source.exists():
                output_pdf.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(pdf_source, output_pdf)
                if self.verbose:
                    print(f"✓ PDF generated: {output_pdf}")
                return True
            else:
                if self.verbose:
                    print("✗ PDF file not generated")
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"Error during compilation: {e}")
            return False
        
        finally:
            # Cleanup temp directory if we created it
            if cleanup:
                shutil.rmtree(working_dir, ignore_errors=True)


class ChessDiagramGenerator:
    """Generate chess diagrams and annotated games"""
    
    def __init__(self, verbose: bool = False):
        self.engine = LaTeXEngine(verbose=verbose)
        self.verbose = verbose
    
    def _generate_latex_preamble(self) -> str:
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
    
    def _generate_latex_postamble(self) -> str:
        """Standard LaTeX postamble"""
        return r"""
\end{document}
"""
    
    def generate_single_diagram(
        self, 
        fen: str, 
        output_pdf: Path,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        board_size: str = "3in"
    ) -> bool:
        """
        Generate a single chess diagram from FEN notation
        
        Args:
            fen: FEN string representing the position
            output_pdf: Where to save the PDF
            title: Optional title for the diagram
            caption: Optional caption below the diagram
            board_size: Size of the chess board (e.g., "3in", "10cm")
        
        Returns:
            True if successful
        """
        latex_content = self._generate_latex_preamble()
        
        if title:
            latex_content += f"\\section*{{{title}}}\n\n"
        
        # Note: Board size is controlled globally by \setchessboard in preamble
        # Individual board sizing would require different parameters per pgfstyle
        latex_content += f"\\chessboard[setfen={fen}]\n\n"
        
        if caption:
            latex_content += f"\\begin{{center}}\\textit{{{caption}}}\\end{{center}}\n\n"
        
        latex_content += self._generate_latex_postamble()
        
        return self.engine.compile(latex_content, output_pdf)
    
    def generate_diagram_at_move(
        self,
        pgn_content: str,
        move_number: int,
        output_pdf: Path,
        title: Optional[str] = None
    ) -> bool:
        """
        Generate diagram showing position after a specific move
        
        Args:
            pgn_content: PGN game as string
            move_number: Which move to show (half-move count, 0-indexed)
            output_pdf: Where to save the PDF
            title: Optional title
        
        Returns:
            True if successful
        """
        try:
            import chess.pgn
            from io import StringIO
            
            pgn = StringIO(pgn_content)
            game = chess.pgn.read_game(pgn)
            
            if not game:
                if self.verbose:
                    print("Failed to parse PGN")
                return False
            
            # Play through to desired move
            board = game.board()
            moves_played = 0
            
            for move in game.mainline_moves():
                if moves_played >= move_number:
                    break
                board.push(move)
                moves_played += 1
            
            fen = board.fen()
            
            if title is None:
                title = f"Position after move {move_number}"
            
            return self.generate_single_diagram(fen, output_pdf, title=title)
            
        except ImportError:
            print("Error: python-chess library required. Install with: pip install chess")
            return False
        except Exception as e:
            if self.verbose:
                print(f"Error generating diagram: {e}")
            return False
    
    def generate_annotated_game(
        self,
        pgn_content: str,
        output_pdf: Path,
        diagrams_at_moves: Optional[List[int]] = None,
        show_final_position: bool = True
    ) -> bool:
        """
        Generate a complete annotated game with diagrams
        
        Args:
            pgn_content: PGN game as string
            output_pdf: Where to save the PDF
            diagrams_at_moves: List of move numbers where diagrams should appear
            show_final_position: Whether to show final position diagram
        
        Returns:
            True if successful
        """
        try:
            import chess.pgn
            from io import StringIO
            
            pgn = StringIO(pgn_content)
            game = chess.pgn.read_game(pgn)
            
            if not game:
                if self.verbose:
                    print("Failed to parse PGN")
                return False
            
            latex_content = self._generate_latex_preamble()
            
            # Add game header
            white = game.headers.get("White", "?")
            black = game.headers.get("Black", "?")
            event = game.headers.get("Event", "")
            date = game.headers.get("Date", "")
            result = game.headers.get("Result", "*")
            
            latex_content += f"\\section*{{{white} vs {black}}}\n\n"
            
            if event:
                latex_content += f"\\textbf{{Event:}} {event}\\\\\n"
            if date:
                latex_content += f"\\textbf{{Date:}} {date}\\\\\n"
            latex_content += f"\\textbf{{Result:}} {result}\n\n"
            
            # Format moves
            moves = []
            board = game.board()
            move_number = 0
            
            for move in game.mainline_moves():
                san = board.san(move)
                moves.append((move_number, san))
                board.push(move)
                move_number += 1
            
            # Generate game with intermediate diagrams
            if diagrams_at_moves:
                # Show complete game with diagrams interspersed
                latex_content += "\\newchessgame\n"
                
                # Show all moves first
                latex_content += "\\mainline{"
                for i, (move_num, move) in enumerate(moves):
                    if i % 2 == 0:  # White's move
                        latex_content += f"{i//2 + 1}. "
                    latex_content += move + " "
                latex_content += "}\n\n"
                
                # Now show diagrams at requested positions
                latex_content += "\\subsection*{Key Positions}\n\n"
                for diagram_move in sorted(diagrams_at_moves):
                    if diagram_move >= len(moves):
                        continue
                    
                    # Start a new game and replay to this position using hidemoves
                    latex_content += "\\newchessgame\n"
                    latex_content += "\\hidemoves{"
                    for i in range(diagram_move + 1):
                        move_num, move = moves[i]
                        if i % 2 == 0:  # White's move
                            latex_content += f"{i//2 + 1}. "
                        latex_content += move + " "
                    latex_content += "}\n"
                    
                    # Show diagram
                    latex_content += f"\\textbf{{Position after move {diagram_move + 1}}}\n\n"
                    latex_content += "\\chessboard\n\n"
            else:
                # Simple case: show all moves at once
                latex_content += "\\newchessgame\n"
                latex_content += "\\mainline{"
                for i, (move_num, move) in enumerate(moves):
                    if i % 2 == 0:  # White's move
                        latex_content += f"{i//2 + 1}. "
                    latex_content += move + " "
                latex_content += "}\n\n"
            
            # Final position
            if show_final_position:
                latex_content += "\\subsection*{Final Position}\n\n"
                latex_content += "\\chessboard\n\n"
            
            latex_content += self._generate_latex_postamble()
            
            return self.engine.compile(latex_content, output_pdf)
            
        except ImportError:
            print("Error: python-chess library required. Install with: pip install chess")
            return False
        except Exception as e:
            if self.verbose:
                print(f"Error generating annotated game: {e}")
            return False


def main():
    """Example usage"""
    print("Chess Diagram Generator - Example Usage\n")
    
    generator = ChessDiagramGenerator(verbose=True)
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Example 1: Single diagram from FEN
    print("\n1. Generating single diagram from FEN...")
    fen = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
    success = generator.generate_single_diagram(
        fen=fen,
        output_pdf=output_dir / "single_diagram.pdf",
        title="Scandinavian Defense",
        caption="After 1.e4 e5 2.Nf3 Nc6"
    )
    print(f"Result: {'Success' if success else 'Failed'}")
    
    print("\nExample completed. Check the 'output' directory for generated PDFs.")
    print("\nFor more examples, see examples/ directory.")


if __name__ == "__main__":
    main()
