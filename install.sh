#!/bin/bash
# ok-claude — Installer
set -e

echo ""
echo "🎙️  ok-claude installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check macOS
if [[ "$(uname)" != "Darwin" ]]; then
  echo "❌ This project is macOS only."
  exit 1
fi

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "❌ Python 3 not found. Install it from https://python.org"
  exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Check / install Homebrew
if ! command -v brew &>/dev/null; then
  echo ""
  echo "📦 Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
echo "✓ Homebrew found"

# Install portaudio (needed by pyaudio)
if ! brew list portaudio &>/dev/null 2>&1; then
  echo ""
  echo "📦 Installing portaudio..."
  brew install portaudio
fi
echo "✓ portaudio found"

# Install Python deps
echo ""
echo "📦 Installing Python packages..."
pip3 install SpeechRecognition pyaudio --quiet
echo "✓ SpeechRecognition installed"
echo "✓ pyaudio installed"

# Make scripts executable
chmod +x wake_word_listener.py
chmod +x scripts/open_tabs.sh
chmod +x raycast/ok_claude.sh
echo "✓ Scripts made executable"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo ""
echo "  1. Edit your URLs in wake_word_listener.py"
echo "     (look for the URLS = [...] section near the top)"
echo ""
echo "  2. Run the listener:"
echo "     python3 wake_word_listener.py"
echo ""
echo "  3. Say \"ok claude\" and watch your tabs open! 🚀"
echo ""
echo "  Optional — auto-start on login:"
echo "     See README.md → 'Run on startup' section"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
