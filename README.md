# 🎙️ ok-claude

> Say **"ok claude"** and your morning tabs open automatically.

A lightweight macOS wake word listener that opens your daily tabs (Gmail, Claude, LinkedIn, Notion, whatever you want) the moment you say the magic words — no clicking, no typing.

---

## ✨ What it does

- 🎤 Listens in the background for your wake phrase
- 🚀 Opens all your URLs in one shot
- 🔧 Fully customizable — change the wake word, URLs, browser, anything
- 💤 Optional: runs on startup so it's always ready

---

## 🖥️ Requirements

- macOS (uses AppleScript to control the browser)
- Python 3.8+
- Internet connection (uses Google Speech Recognition)

---

## ⚡ Quick start

```bash
git clone https://github.com/YOUR_USERNAME/ok-claude.git
cd ok-claude
./install.sh
```

Then edit your URLs in `wake_word_listener.py`:

```python
URLS = [
    "https://claude.ai",
    "https://mail.google.com",
    "https://linkedin.com/feed",
    "https://notion.so",
    # add yours here
]
```

Then run it:

```bash
python3 wake_word_listener.py
```

Say **"ok claude"** → tabs open. That's it.

---

## ⚙️ Configuration

You can customize everything either in the script itself, or by creating `~/.ok-claude.json`:

```json
{
  "wake_words": ["ok claude", "okay claude", "morning routine"],
  "browser": "Google Chrome",
  "cooldown_seconds": 5,
  "urls": [
    "https://claude.ai",
    "https://mail.google.com",
    "https://linkedin.com/feed",
    "https://notion.so"
  ]
}
```

| Option | Default | Description |
|---|---|---|
| `wake_words` | `["ok claude", "okay claude"]` | Phrases that trigger the launcher |
| `browser` | `"Google Chrome"` | Browser to open tabs in (`Safari`, `Arc`, `Firefox`, `Brave Browser`) |
| `cooldown_seconds` | `5` | Seconds before it can trigger again |
| `urls` | see script | List of URLs to open |

---

## 🚀 No-voice version (Raycast / keyboard shortcut)

Don't want always-on listening? Just use the shell script:

```bash
bash scripts/open_tabs.sh
```

**Raycast integration:**
1. Open Raycast → Extensions → Script Commands
2. Add the `raycast/` folder
3. Search "Ok Claude" and run it (or assign a hotkey)

---

## 🔄 Run on startup

To have ok-claude start automatically when you log in:

1. Open **Script Editor** on your Mac
2. Paste this and save as an Application:

```applescript
do shell script "cd /path/to/ok-claude && python3 wake_word_listener.py &> /tmp/ok-claude.log &"
```

3. Go to **System Settings → General → Login Items** and add the app.

Or use a launchd plist — see [Apple's docs](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html).

---

## 🔒 Privacy

- Uses **Google Speech Recognition** — audio snippets are sent to Google's API for transcription (same as pressing the mic in Google Search)
- If you want fully offline/private recognition, swap in [Vosk](https://alphacephei.com/vosk/) — it runs locally with no internet needed

---

## 🛠️ Troubleshooting

**"No module named speech_recognition"**
```bash
pip3 install SpeechRecognition pyaudio
```

**pyaudio install fails**
```bash
brew install portaudio
pip3 install pyaudio
```

**Mic not working / always mishearing**
- Grant microphone access: System Settings → Privacy & Security → Microphone → Terminal ✓
- Adjust `recognizer.energy_threshold` in the script (lower = more sensitive)

**Browser not opening**
- Make sure the browser name in `BROWSER` exactly matches the app name in your `/Applications` folder

---

## 📁 Project structure

```
ok-claude/
├── wake_word_listener.py   # main voice listener
├── scripts/
│   └── open_tabs.sh        # simple shell launcher (no voice)
├── raycast/
│   └── ok_claude.sh        # Raycast script command
├── config.example.json     # example config file
├── install.sh              # one-command installer
└── README.md
```

---

## 🤝 Contributing

PRs welcome! Ideas for future versions:
- [ ] Offline wake word detection (Vosk / Porcupine)
- [ ] Menu bar icon with status indicator
- [ ] Per-profile URL sets (work mode vs personal mode)
- [ ] Slack / Discord notifications on trigger

---

## 📄 License

MIT — do whatever you want with it.

---

*Built with Python + AppleScript + a little Claude magic ✨*
