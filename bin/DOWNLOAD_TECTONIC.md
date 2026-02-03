# How to Download Tectonic Binaries

For this application to work, you need to download Tectonic binaries for each platform you want to support.

## Download Links (Version 0.15.0 or later)

Visit: https://github.com/tectonic-typesetting/tectonic/releases/latest

### For Linux (x86_64)
1. Download: `tectonic-0.15.0-x86_64-unknown-linux-musl.tar.gz`
2. Extract the `tectonic` binary
3. Place in: `bin/linux/tectonic`
4. Make executable: `chmod +x bin/linux/tectonic`

### For Windows (x86_64)
1. Download: `tectonic-0.15.0-x86_64-pc-windows-msvc.zip`
2. Extract `tectonic.exe`
3. Place in: `bin/windows/tectonic.exe`

### For macOS (Intel)
1. Download: `tectonic-0.15.0-x86_64-apple-darwin.tar.gz`
2. Extract the `tectonic` binary
3. Place in: `bin/macos/tectonic`
4. Make executable: `chmod +x bin/macos/tectonic`

### For macOS (Apple Silicon/M1/M2)
1. Download: `tectonic-0.15.0-aarch64-apple-darwin.tar.gz`
2. Extract the `tectonic` binary  
3. Place in: `bin/macos/tectonic`
4. Make executable: `chmod +x bin/macos/tectonic`

## Verification

After downloading, your directory structure should look like:

```
chess_diagram_app/
├── bin/
│   ├── linux/
│   │   └── tectonic          (~50 MB)
│   ├── windows/
│   │   └── tectonic.exe      (~50 MB)
│   └── macos/
│       └── tectonic          (~50 MB)
├── chess_generator.py
└── ...
```

## Alternative: System Installation

Users can also install Tectonic system-wide instead of using bundled binaries:

```bash
# Linux/macOS with Homebrew
brew install tectonic

# Arch Linux
pacman -S tectonic

# From source (requires Rust)
cargo install tectonic
```

The application will automatically detect and use system-installed Tectonic if bundled binaries are not found.
