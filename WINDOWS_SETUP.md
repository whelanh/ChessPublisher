# Windows VM Setup and Testing Guide

This guide walks you through setting up a fresh Windows machine to use ChessPublisher.

## Step 1: Install Python

1. Download Python from https://www.python.org/downloads/windows/
2. Run the installer
3. **IMPORTANT**: Check ✅ "Add Python to PATH" at the bottom of the installer
4. Click "Install Now"

Verify installation by opening Command Prompt (Win+R, type `cmd`, press Enter):
```cmd
python --version
```

## Step 2: Install LaTeX Distribution

### Option A: MiKTeX (Recommended)

MiKTeX is recommended for Windows - it's faster to install and automatically downloads packages as needed.

1. Download from https://miktex.org/download
2. Run the installer
3. Choose **"Install missing packages on-the-fly: Yes"** (important!)
4. Complete installation (~5-10 minutes)

After installation, open a **new** Command Prompt and verify:
```cmd
pdflatex --version
```

### Option B: TeX Live (Alternative)

TeX Live provides a complete LaTeX distribution but takes significantly longer to install (~2 hours for a full installation).

1. Download the installer from https://tug.org/texlive/acquire-netinstall.html
2. Run the installer and follow prompts
3. For a smaller install, click "Advanced" and select "basic" scheme

## Step 3: Install LaTeX Chess Packages

Open Command Prompt (run as Administrator if you encounter permission issues):

**For MiKTeX** (pre-install packages to avoid prompts during use):
```cmd
mpm --install=xskak
mpm --install=chessboard
mpm --install=chessfss
mpm --install=skak
```

**For TeX Live:**
```cmd
tlmgr install xskak chessboard chessfss skak
```

## Step 4: Get ChessPublisher

### Option A: Clone with Git
If you have Git installed:
```cmd
git clone https://github.com/whelanh/chessPublisher.git
cd chessPublisher
```

### Option B: Download ZIP
Download the repository as a ZIP from GitHub and extract it.

### Option C: Copy from shared folder
If using a VM with a shared folder, copy the `chessPublisher` folder (e.g., to `C:\chess\chessPublisher`).

## Step 5: Install Python Dependencies

Open Command Prompt and navigate to the project:
```cmd
cd C:\path\to\chessPublisher
pip install -r requirements.txt
```

This installs the `chess` library for PGN parsing.

## Step 6: Run Tests

### Test 1: Run the Windows Test Script
```cmd
python test_windows.py
```

This tests basic diagram generation, tex_only mode, and annotated games.

### Test 2: Run All Examples
```cmd
python examples/all_examples.py
```

This should generate 8 PDF files in the `output/` directory.

**Note:** Do NOT use `verify_setup.py` on Windows - it may report false errors. Use `test_windows.py` or `examples/all_examples.py` instead.

## Expected Results

✅ All examples should complete without "I can't find file" errors
✅ PDF files should be generated in the `output/` folder
✅ The `tex_only=True` option should create `.tex` files instead of PDFs

## Troubleshooting

### "python is not recognized"
- Reinstall Python and make sure to check "Add Python to PATH"
- Or manually add Python to PATH: Search "Environment Variables" → Edit PATH → Add Python install directory

### "pdflatex is not recognized"
- Restart Command Prompt after installing MiKTeX or TeX Live
- For TeX Live, add `C:\texlive\2024\bin\windows` to your PATH

### MiKTeX package prompts during compilation
- Run the `mpm --install=...` commands from Step 3 to pre-install packages
- Or allow MiKTeX to install packages automatically when prompted

### "I can't find file" errors with paths containing ~
- This should be fixed automatically now
- If it persists, try moving the project to a simple path like `C:\chess\chessPublisher`

### Package not found errors
- For MiKTeX: Open MiKTeX Console → Updates → Check for updates, then re-run the mpm install commands
- For TeX Live: Run `tlmgr install xskak chessboard chessfss skak`

### Permission errors
- Don't run from `C:\Program Files` or other protected directories
- Use a folder like `C:\chess\` or your Documents folder

## Quick Test

The repository includes `test_windows.py` - just run:
```cmd
python test_windows.py
```

This will test PDF generation, tex_only mode, and annotated games, then report PASS/FAIL for each.
