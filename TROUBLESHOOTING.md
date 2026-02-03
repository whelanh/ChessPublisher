# Troubleshooting Guide - Chess Diagram Generator

This guide helps you resolve common issues when setting up and using the Chess Diagram Generator.

## Quick Diagnosis

Run the setup verification script first:

```bash
python3 verify_setup.py
```

This will identify which components are missing or misconfigured.

---

## Common Issues

### 1. LaTeX Error: "File 'xskak.sty' not found"

**Symptoms:**
- Error message: `! LaTeX Error: File 'xskak.sty' not found.`
- Diagrams fail to generate

**Cause:**
Tectonic needs to download the `xskak` LaTeX package from the internet on first use.

**Solutions:**

#### Solution A: Ensure Internet Connection (Recommended)
1. Check your internet connection
2. Run the verification script to trigger package download:
   ```bash
   python3 verify_setup.py
   ```
3. Wait for packages to download (may take 30-60 seconds on first run)
4. Try generating diagrams again

#### Solution B: Pre-cache Packages
If you have intermittent internet, pre-download packages:

```bash
# Create a test LaTeX file
cat > test.tex << 'EOF'
\documentclass{article}
\usepackage{xskak}
\usepackage{chessboard}
\begin{document}
Test
\end{document}
EOF

# Compile it (this downloads packages)
tectonic -X compile test.tex

# Clean up
rm test.tex test.pdf
```

After this, packages are cached and work offline.

#### Solution C: Proxy/Firewall Issues
If behind a corporate firewall or proxy:

```bash
# Set proxy environment variables
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port

# Then run verification
python3 verify_setup.py
```

---

### 2. "Tectonic not found" Error

**Symptoms:**
- Error: `Tectonic not found. Please either...`
- Application won't start

**Solutions by Platform:**

#### Linux

**Option 1: Using Homebrew (Linuxbrew)**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Tectonic
brew install tectonic
```

**Option 2: Using Package Manager**
```bash
# Fedora
sudo dnf install tectonic

# Arch Linux
sudo pacman -S tectonic

# Ubuntu/Debian (manual install required)
# Download from: https://github.com/tectonic-typesetting/tectonic/releases/latest
wget https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic@0.15.0/tectonic-0.15.0-x86_64-unknown-linux-gnu.tar.gz
tar xzf tectonic-0.15.0-x86_64-unknown-linux-gnu.tar.gz
sudo mv tectonic /usr/local/bin/
sudo chmod +x /usr/local/bin/tectonic
```

**Option 3: Using Bundled Binary**
See `bin/DOWNLOAD_TECTONIC.md` for instructions on downloading the bundled binary.

#### macOS

**Option 1: Using Homebrew (Recommended)**
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Tectonic
brew install tectonic
```

**Option 2: Using Bundled Binary**
See `bin/DOWNLOAD_TECTONIC.md`

#### Windows

**Option 1: Using Scoop**
```powershell
# Install Scoop if needed
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install Tectonic
scoop bucket add extras
scoop install tectonic
```

**Option 2: Using Bundled Binary**
See `bin/DOWNLOAD_TECTONIC.md`

---

### 3. "No module named 'chess'" Error

**Symptoms:**
- ImportError when running examples
- Error: `No module named 'chess'`

**Solution:**
Install the python-chess library:

```bash
# Using pip
pip install chess

# Or using pip3
pip3 install chess

# Or from requirements.txt
pip install -r requirements.txt
```

**Verify installation:**
```bash
python3 -c "import chess; print(chess.__version__)"
```

---

### 4. Permission Denied (Linux/macOS)

**Symptoms:**
- Error: `Permission denied` when running bundled Tectonic
- Binary won't execute

**Solution:**
Make the binary executable:

```bash
# For Linux
chmod +x bin/linux/tectonic

# For macOS
chmod +x bin/macos/tectonic

# macOS may also require removing quarantine attribute
xattr -d com.apple.quarantine bin/macos/tectonic
```

---

### 5. Diagrams Generate But Are Blank

**Symptoms:**
- PDF is created successfully
- PDF contains title but no chess board

**Possible Causes & Solutions:**

#### Invalid FEN String
```python
# Bad - invalid FEN
fen = "rnbqkbnr/pppppppp/8/8/PPPPPPPP/RNBQKBNR"  # Missing parts

# Good - complete FEN
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
```

#### Corrupted LaTeX Package Cache
```bash
# Clear Tectonic cache and re-download
rm -rf ~/.cache/Tectonic
python3 verify_setup.py
```

---

### 6. LaTeX Compilation Timeout

**Symptoms:**
- Process hangs for a long time
- Eventually fails or times out

**Causes:**
- First-time package download
- Slow internet connection

**Solutions:**

1. **Be patient on first run** - Initial package download can take 1-2 minutes
2. **Check internet speed** - Tectonic downloads ~50MB of packages
3. **Increase timeout** in `chess_generator.py`:
   ```python
   # In TectonicEngine.compile(), change timeout
   result = subprocess.run(
       [...],
       timeout=120  # Increase from 60 to 120 seconds
   )
   ```

---

### 7. Windows-Specific Issues

#### PowerShell Execution Policy
```powershell
# If scripts won't run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Long Path Issues
Windows has a 260-character path limit. Use short directory names:

```powershell
# Bad
C:\Users\YourName\Documents\Projects\MyProjects\chess_diagram_generator\output\

# Good
C:\chess\output\
```

---

### 8. macOS Security Warning

**Symptoms:**
- "tectonic cannot be opened because it is from an unidentified developer"

**Solution:**

```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine bin/macos/tectonic

# Or, in System Preferences:
# 1. Open System Preferences > Security & Privacy
# 2. Click "Open Anyway" next to the Tectonic message
```

---

## Offline Usage

To use the application without internet access:

1. **First-time setup with internet:**
   ```bash
   python3 verify_setup.py
   ```
   This downloads all required LaTeX packages (~50MB) to Tectonic's cache.

2. **Verify offline capability:**
   ```bash
   # Disconnect from internet
   python3 examples/all_examples.py
   ```

3. **Package cache location:**
   - Linux: `~/.cache/Tectonic/`
   - macOS: `~/Library/Caches/Tectonic/`
   - Windows: `%LOCALAPPDATA%\Tectonic\`

---

## Platform-Specific Package Locations

If you need to manually inspect or clear package caches:

### Linux
```bash
# Cache location
~/.cache/Tectonic/

# View cached packages
ls -lah ~/.cache/Tectonic/

# Clear cache
rm -rf ~/.cache/Tectonic/
```

### macOS
```bash
# Cache location
~/Library/Caches/Tectonic/

# View cached packages
ls -lah ~/Library/Caches/Tectonic/

# Clear cache
rm -rf ~/Library/Caches/Tectonic/
```

### Windows
```powershell
# Cache location
%LOCALAPPDATA%\Tectonic\

# View cached packages
dir %LOCALAPPDATA%\Tectonic\

# Clear cache
rmdir /s /q %LOCALAPPDATA%\Tectonic\
```

---

## Advanced Troubleshooting

### Enable Verbose Mode

```python
# In your script
generator = ChessDiagramGenerator(verbose=True)
```

This shows:
- LaTeX compilation output
- Error messages from Tectonic
- File locations

### Manual LaTeX Compilation

Debug LaTeX issues directly:

```bash
# Generate LaTeX manually
cat > test.tex << 'EOF'
\documentclass{article}
\usepackage{xskak}
\usepackage{chessboard}
\begin{document}
\chessboard[setfen=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1]
\end{document}
EOF

# Compile and see detailed output
tectonic -X compile test.tex
```

### Check Tectonic Version

```bash
tectonic --version
```

Minimum recommended version: 0.15.0

### Network Debugging

Test if Tectonic can reach package servers:

```bash
# Test network connectivity to CTAN
curl -I https://ctan.org/

# Test Tectonic package download
tectonic -X compile --print-downloads test.tex
```

---

## Getting Help

If you're still experiencing issues:

1. **Run diagnostics:**
   ```bash
   python3 verify_setup.py > setup_log.txt 2>&1
   ```

2. **Gather information:**
   - Operating system and version
   - Python version (`python3 --version`)
   - Tectonic version (`tectonic --version`)
   - Error messages from `setup_log.txt`

3. **Common error patterns:**
   - Network issues: Check firewall/proxy settings
   - Permission issues: Check file/directory permissions
   - Package issues: Clear cache and retry

4. **Create an issue:**
   Include the diagnostics output and error messages in your bug report.

---

## Prevention: Pre-flight Checklist

Before deploying to new users:

- [ ] Run `python3 verify_setup.py` successfully
- [ ] Generate at least one example diagram
- [ ] Test offline (disconnect internet and generate)
- [ ] Document any platform-specific quirks
- [ ] Include setup verification in your README

---

## FAQ

**Q: Do I need a full LaTeX installation?**  
A: No! Tectonic is self-contained and doesn't require TeX Live or MikTeX.

**Q: How much disk space is needed?**  
A: ~100MB (50MB for Tectonic binary + 50MB for LaTeX packages)

**Q: Can I use this in CI/CD pipelines?**  
A: Yes! Install Tectonic in your CI environment:
```yaml
# GitHub Actions example
- name: Install Tectonic
  run: |
    brew install tectonic  # or apt-get, etc.
```

**Q: Does this work in Docker containers?**  
A: Yes! Example Dockerfile:
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y wget
RUN wget https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic@0.15.0/tectonic-0.15.0-x86_64-unknown-linux-gnu.tar.gz
RUN tar xzf tectonic-*.tar.gz && mv tectonic /usr/local/bin/
RUN pip install chess
```

**Q: Can I customize the chess board appearance?**  
A: Yes! Edit the `\setchessboard{}` settings in `chess_generator.py`.

---

## Additional Resources

- **Tectonic Documentation:** https://tectonic-typesetting.github.io/
- **xskak Package:** https://ctan.org/pkg/xskak
- **python-chess Documentation:** https://python-chess.readthedocs.io/
- **FEN Notation:** https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
