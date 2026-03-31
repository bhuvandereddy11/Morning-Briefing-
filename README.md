# Morning Briefing

> **Sunday fun project — vibe coded in under 20 minutes. Don't expect production quality.**

> Say **"good morning"** and your Mac reads your notifications aloud.

A lightweight macOS wake word listener that delivers a spoken morning briefing — app badge counts and unread iMessages — the moment you say the magic words.

---

## What it does

- Listens in the background for **"good morning"** (works with "hey claude good morning", "good morning claude", etc.)
- Reads aloud unread notification badge counts for: **Messages, Mail, Slack, WhatsApp, Telegram**
- Reads your **unread iMessage count**
- Prevents re-triggering while speaking (no feedback loops)
- 30-second cooldown after each briefing

---

## Requirements

| Requirement | Version | Notes |
|---|---|---|
| macOS | Any recent version | Uses AppleScript + `say` command |
| Python | 3.8+ | `python3 --version` to check |
| Homebrew | Latest | Package manager for macOS |
| portaudio | Latest | C library for microphone access |
| SpeechRecognition | Python package | Wake word detection via Google |
| pyaudio | Python package | Python bindings for portaudio |
| Internet connection | — | Required for Google Speech Recognition |

---

## macOS Permissions Required

Before running, grant these in **System Settings → Privacy & Security**:

| Permission | Where | Why |
|---|---|---|
| **Microphone** | Privacy & Security → Microphone → Terminal ✓ | Listens for wake phrase |
| **Accessibility** | Privacy & Security → Accessibility → Terminal ✓ | AppleScript reads app badge counts |

> If you run from VS Code or another terminal app, grant permissions to that app instead of Terminal.

---

## Installation

**Step 1 — Clone the repo:**
```bash
git clone https://github.com/bhuvandereddy11/Morning-Briefing-.git
cd Morning-Briefing-
```

**Step 2 — Run the installer (installs all dependencies automatically):**
```bash
./install.sh
```

This installs: Homebrew (if missing) → portaudio → SpeechRecognition → pyaudio

**Or install manually:**
```bash
brew install portaudio
pip3 install SpeechRecognition pyaudio
```

---

## Running

```bash
python3 wake_word_listener.py
```

You should see:
```
🎙️  ok-claude is listening...
   Morning trigger: "hey/hi claude good morning"
   Press Ctrl+C to stop

✓ Calibrated to ambient noise. Ready!
```

Say **"good morning"** → briefing plays through your speakers.

Press **Ctrl+C** to stop.

---

## Configuration

### Option 1 — Edit the script directly

Open [wake_word_listener.py](wake_word_listener.py) and change the values at the top:

```python
MORNING_WORDS = ["good morning"]   # add more trigger phrases here
COOLDOWN_SECONDS = 30              # seconds before it can trigger again
LANGUAGE = "en-US"                 # speech recognition language
```

### Option 2 — Config file (no code editing)

Create `~/.ok-claude.json` (in your home folder, not the project folder):

```json
{
  "morning_words": ["good morning", "morning briefing"],
  "cooldown_seconds": 30
}
```

| Option | Default | Description |
|---|---|---|
| `morning_words` | `["good morning"]` | Phrases that trigger the briefing |
| `cooldown_seconds` | `30` | Seconds before it can trigger again |

---

## Adding / changing which apps are monitored

Open [wake_word_listener.py](wake_word_listener.py) and find the `get_mac_notifications()` function:

```python
apps = {
    "Messages":  "iMessage",
    "Mail":      "Mail",
    "Slack":     "Slack",
    "WhatsApp":  "WhatsApp",
    "Telegram":  "Telegram",
}
```

- The **key** (`"Messages"`) must exactly match the app name in your `/Applications` folder
- The **value** (`"iMessage"`) is what gets spoken aloud
- Add or remove lines to change which apps are checked

---

## Run on startup

1. Open **Script Editor** on your Mac
2. Paste this (update the path to match where you cloned the repo):

```applescript
do shell script "cd /Users/YOUR_USERNAME/Morning-Briefing- && python3 wake_word_listener.py &> /tmp/morning-briefing.log &"
```

3. Save as an Application (File → Save → File Format: Application)
4. Go to **System Settings → General → Login Items** → add the saved app

---

## Privacy

- Uses **Google Speech Recognition** — short audio clips are sent to Google's servers for transcription (same as Google Search mic)
- No audio is stored — only the transcribed text is used locally
- For fully offline/private recognition, swap in [Vosk](https://alphacephei.com/vosk/) (no internet needed)

---

## Troubleshooting

**"No module named speech_recognition"**
```bash
pip3 install SpeechRecognition pyaudio
```

**pyaudio install fails**
```bash
brew install portaudio
pip3 install pyaudio
```

**Mic not detected / OSError**
- Grant Terminal microphone access: System Settings → Privacy & Security → Microphone
- The script auto-reconnects if the mic disconnects — just wait 2 seconds

**Always mishearing the trigger**
- Speak clearly and include "good morning" — it matches any phrase containing those words
- Lower `recognizer.energy_threshold` in the script (default 300 — try 200 in a quiet room)

**Badge counts not showing for an app**
- The app must be running and have the Accessibility permission granted
- Grant it: System Settings → Privacy & Security → Accessibility → Terminal ✓

**Briefing triggers again mid-speech**
- The 30-second cooldown and `is_speaking` flag should prevent this
- If it still happens, increase `COOLDOWN_SECONDS` in the script

---

## Project structure

```
Morning-Briefing-/
├── wake_word_listener.py   # main listener + morning briefing logic
├── config.example.json     # example config file
├── install.sh              # one-command installer
└── README.md
```

---

## License

MIT — do whatever you want with it.

---

*Built with Python + AppleScript + a little Claude magic*
