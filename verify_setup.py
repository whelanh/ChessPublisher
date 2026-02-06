#!/usr/bin/env python3
"""
Setup Verification Script for Chess Diagram Generator

This script verifies that all dependencies are properly installed,
including LaTeX packages required for chess diagram generation.
"""

import subprocess
import sys
import shutil
from pathlib import Path
import tempfile


def check_python_version():
    """Verify Python version is 3.7+"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (need 3.7+)")
        return False


def check_python_chess():
    """Verify python-chess is installed"""
    print("\nChecking python-chess library...")
    try:
        import chess
        print(f"  ✓ python-chess {chess.__version__}")
        return True
    except ImportError:
        print("  ✗ python-chess not found")
        print("    Install with: pip install chess")
        return False


def check_latex_engine():
    """Verify LaTeX engine is available (pdflatex, xelatex, or tectonic)"""
    print("\nChecking LaTeX engine...")
    
    # Check for pdflatex (preferred)
    pdflatex = shutil.which('pdflatex')
    if pdflatex:
        try:
            result = subprocess.run(
                ['pdflatex', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"  ✓ pdflatex: {version_line}")
                return True, 'pdflatex'
        except Exception as e:
            print(f"  ⚠ Found pdflatex but couldn't get version: {e}")
    
    # Check for xelatex (alternative)
    xelatex = shutil.which('xelatex')
    if xelatex:
        try:
            result = subprocess.run(
                ['xelatex', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"  ✓ xelatex: {version_line}")
                return True, 'xelatex'
        except Exception as e:
            print(f"  ⚠ Found xelatex but couldn't get version: {e}")
    
    # Check for tectonic (fallback, but not recommended)
    tectonic = shutil.which('tectonic')
    if tectonic:
        try:
            result = subprocess.run(
                ['tectonic', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"  ✓ tectonic: {version}")
                print("    Note: Tectonic found but TeX Live is recommended")
                return True, 'tectonic'
        except Exception as e:
            print(f"  ⚠ Found tectonic but couldn't get version: {e}")
    
    print("  ✗ No LaTeX engine found")
    print("    Install TeX Live (recommended):")
    print("      Fedora/RHEL: sudo dnf install texlive-scheme-basic texlive-xskak texlive-chessboard texlive-parskip")
    print("      Ubuntu/Debian: sudo apt-get install texlive-games texlive-latex-extra")
    print("      macOS: brew install --cask basictex")
    return False, None


def check_latex_packages(latex_engine):
    """Verify xskak and chessboard packages are available"""
    print("\nChecking LaTeX chess packages...")
    
    # Create a minimal test document
    test_latex = r"""\documentclass{article}
\usepackage{xskak}
\usepackage{chessboard}
\begin{document}
Test
\end{document}
"""
    
    # Try to compile in a temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        tex_file = tmpdir / 'test.tex'
        tex_file.write_text(test_latex, encoding='utf-8')
        
        try:
            # Build command based on engine type
            if latex_engine == 'tectonic':
                cmd = ['tectonic', '-X', 'compile', str(tex_file)]
            else:
                # pdflatex or xelatex - use batch mode and halt on error
                cmd = [latex_engine, '-interaction=nonstopmode', '-halt-on-error', str(tex_file.name)]
            
            result = subprocess.run(
                cmd,
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=60  # Give it time to download packages (MiKTeX) or process
            )
            
            if result.returncode == 0:
                print("  ✓ xskak package available")
                print("  ✓ chessboard package available")
                return True
            else:
                print("  ✗ Failed to load chess packages")
                print("\nError output:")
                # Show last 20 lines of output for debugging
                error_lines = result.stdout.split('\n')[-20:]
                print('\n'.join(error_lines))
                
                # Check for specific errors
                combined_output = result.stdout + result.stderr
                if 'xskak.sty' in combined_output or "can't find file `xskak.sty'" in combined_output:
                    print("\n  Issue: xskak.sty not found")
                    print("  Solution: Install chess packages:")
                    print("    Fedora/RHEL: sudo dnf install texlive-xskak texlive-chessboard")
                    print("    Ubuntu/Debian: sudo apt-get install texlive-games")
                    print("    macOS: sudo tlmgr install xskak chessboard")
                if 'chessboard.sty' in combined_output or "can't find file `chessboard.sty'" in combined_output:
                    print("\n  Issue: chessboard.sty not found")
                
                return False
                
        except subprocess.TimeoutExpired:
            print("  ⚠ Compilation timed out (packages may be downloading)")
            print("    Try running verify_setup.py again in a few moments")
            return False
        except Exception as e:
            print(f"  ✗ Error testing packages: {e}")
            return False


def test_diagram_generation():
    """Test actual diagram generation"""
    print("\nTesting diagram generation...")
    
    try:
        from chess_generator import ChessDiagramGenerator
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            output_path = tmpdir / 'test.pdf'
            
            generator = ChessDiagramGenerator(verbose=False)
            success = generator.generate_single_diagram(
                fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                output_path=output_path,
                title="Test Diagram"
            )
            
            if success and output_path.exists():
                print("  ✓ Successfully generated test diagram")
                return True
            else:
                print("  ✗ Failed to generate test diagram")
                return False
                
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def print_summary(results):
    """Print summary of verification results"""
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = all(results.values())
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check}")
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All checks passed! Your setup is ready to use.")
        print("\nTry running: python examples/all_examples.py")
    else:
        print("\n⚠️  Some checks failed. Please review the errors above.")
        print("\nCommon solutions:")
        print("  1. Install python-chess: pip install chess")
        print("  2. Install TeX Live:")
        print("       Fedora/RHEL: sudo dnf install texlive-scheme-basic texlive-xskak texlive-chessboard texlive-parskip")
        print("       Ubuntu/Debian: sudo apt-get install texlive-games texlive-latex-extra")
        print("       macOS: brew install --cask basictex")
        print("  3. See TROUBLESHOOTING.md for more help")
    
    return all_passed


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Chess Diagram Generator - Setup Verification")
    print("=" * 60)
    
    results = {}
    
    # Check Python version
    results['Python 3.7+'] = check_python_version()
    
    # Check python-chess
    results['python-chess library'] = check_python_chess()
    
    # Check LaTeX engine
    latex_ok, latex_engine = check_latex_engine()
    results['LaTeX engine (pdflatex/xelatex/tectonic)'] = latex_ok
    
    # Check LaTeX packages (only if LaTeX engine is available)
    if latex_ok:
        results['LaTeX chess packages'] = check_latex_packages(latex_engine)
        
        # Test diagram generation (only if packages are OK)
        if results['LaTeX chess packages']:
            results['Diagram generation'] = test_diagram_generation()
    else:
        print("\nSkipping LaTeX package checks (no LaTeX engine available)")
    
    # Print summary
    all_passed = print_summary(results)
    
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
