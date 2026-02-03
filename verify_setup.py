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


def check_tectonic():
    """Verify Tectonic is available"""
    print("\nChecking Tectonic LaTeX engine...")
    
    # Check system installation
    system_tectonic = shutil.which('tectonic')
    if system_tectonic:
        try:
            result = subprocess.run(
                ['tectonic', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"  ✓ System Tectonic: {version}")
                return True, system_tectonic
        except Exception as e:
            print(f"  ⚠ Found Tectonic but couldn't get version: {e}")
    
    # Check bundled binary
    base_dir = Path(__file__).parent
    platform = 'windows' if sys.platform == 'win32' else 'macos' if sys.platform == 'darwin' else 'linux'
    bundled_path = base_dir / 'bin' / platform / ('tectonic.exe' if platform == 'windows' else 'tectonic')
    
    if bundled_path.exists():
        print(f"  ✓ Bundled Tectonic: {bundled_path}")
        return True, str(bundled_path)
    
    print("  ✗ Tectonic not found")
    print("    Install with: brew install tectonic")
    print("    Or download binaries: see bin/DOWNLOAD_TECTONIC.md")
    return False, None


def check_latex_packages(tectonic_path):
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
            result = subprocess.run(
                [tectonic_path, '-X', 'compile', str(tex_file)],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=60  # Give it time to download packages
            )
            
            if result.returncode == 0:
                print("  ✓ xskak package available")
                print("  ✓ chessboard package available")
                return True
            else:
                print("  ✗ Failed to load chess packages")
                print("\nError output:")
                print(result.stderr)
                
                # Check for specific errors
                if 'xskak.sty' in result.stderr:
                    print("\n  Issue: xskak.sty not found")
                    print("  Solution: Ensure internet connection for package download")
                if 'chessboard.sty' in result.stderr:
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
            output_pdf = tmpdir / 'test.pdf'
            
            generator = ChessDiagramGenerator(verbose=False)
            success = generator.generate_single_diagram(
                fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                output_pdf=output_pdf,
                title="Test Diagram"
            )
            
            if success and output_pdf.exists():
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
        print("  2. Install Tectonic: brew install tectonic")
        print("  3. Ensure internet connection (for LaTeX package downloads)")
        print("  4. See TROUBLESHOOTING.md for more help")
    
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
    
    # Check Tectonic
    tectonic_ok, tectonic_path = check_tectonic()
    results['Tectonic LaTeX engine'] = tectonic_ok
    
    # Check LaTeX packages (only if Tectonic is available)
    if tectonic_ok:
        results['LaTeX chess packages'] = check_latex_packages(tectonic_path)
        
        # Test diagram generation (only if packages are OK)
        if results['LaTeX chess packages']:
            results['Diagram generation'] = test_diagram_generation()
    else:
        print("\nSkipping LaTeX package checks (Tectonic not available)")
    
    # Print summary
    all_passed = print_summary(results)
    
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
