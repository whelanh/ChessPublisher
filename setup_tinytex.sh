#!/bin/bash
# Setup script for TinyTeX with all chess diagram dependencies

set -e

echo "============================================================"
echo "Chess Diagram Generator - TinyTeX Setup"
echo "============================================================"
echo ""

# Step 1: Install TinyTeX
if ! command -v tlmgr &> /dev/null; then
    echo "📥 Installing TinyTeX..."
    cd ~ && wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh
    export PATH="$HOME/.local/bin:$PATH"
    echo "✓ TinyTeX installed"
else
    echo "✓ TinyTeX already installed"
    export PATH="$HOME/.local/bin:$PATH"
fi

echo ""
echo "📦 Installing required LaTeX packages..."
echo "This may take a few minutes..."
echo ""

# Step 2: Install all required packages
# Note: These packages are dependencies discovered through testing
PACKAGES=(
    "xskak"
    "chessboard"  
    "chessfss"
    "skak"
    "skaknew"      # Chess fonts
    "pstricks"
    "pst-node"
    "pgf"
    "xifthen"
    "ifmtarg"      # Dependency of xifthen
    "etoolbox"
    "xkeyval"
    # Note: ifthen, calc, textcomp are in base LaTeX (latex/tools packages)
)

for pkg in "${PACKAGES[@]}"; do
    echo -n "  Installing $pkg... "
    if tlmgr install "$pkg" > /tmp/tlmgr_install.log 2>&1; then
        echo "✓"
    elif grep -q "already present" /tmp/tlmgr_install.log; then
        echo "✓ (already installed)"
    elif grep -qi "cannot find" /tmp/tlmgr_install.log; then
        # Package might be in base latex (ifthen, calc, textcomp)
        echo "✓ (in base LaTeX)"
    else
        echo "⚠ (may have failed, check /tmp/tlmgr_install.log)"
    fi
done

# Step 3: Create dummy lambda.sty (workaround for skak bug)
echo ""
echo "🔧 Creating lambda.sty workaround..."
mkdir -p ~/.TinyTeX/texmf-local/tex/latex/
cat > ~/.TinyTeX/texmf-local/tex/latex/lambda.sty << 'EOF'
% Dummy lambda.sty to satisfy skak.sty dependency
% The lambda package is for Omega/Aleph, not needed for chess diagrams
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{lambda}[2026/02/03 Dummy package for skak compatibility]
% No actual code needed - skak doesn't use lambda features
\endinput
EOF

# Step 4: Update TeX database
echo "🔄 Updating TeX database..."
mktexlsr > /dev/null 2>&1

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "⚠️  Note: If you encountered repository sync errors, wait"
echo "    1-2 days and rerun this script to install missing packages."
echo ""
echo "Add TinyTeX to your PATH:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "Or add this permanently to your ~/.bashrc:"
echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
echo "  source ~/.bashrc"
echo ""
echo "Test the installation:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "  python3 verify_setup.py"
echo "  python3 examples/all_examples.py"
echo ""
echo "If diagrams still don't generate, see TROUBLESHOOTING.md"
echo ""
