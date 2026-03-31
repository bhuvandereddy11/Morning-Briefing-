# Morning Briefing

> Say **"good morning"** and your Mac reads your notifications aloud.

A lightweight macOS wake word listener that delivers a spoken morning briefing — app badge counts, unread iMessages — the moment you say the magic words.

---

## What it does

- Listens in the background for "good morning" (or "hey claude good morning")
- Reads aloud your unread notification counts from Messages, Mail, Slack, WhatsApp, Telegram
- Reads your unread iMessage count
- Blocks re-triggering while speaking (no feedback loops)
- 30-second cooldown after each briefing

---

## Requirements

- macOS
- Python 3.8+
- Internet connection (uses Google Speech Recognition)

---

## Quick start

```bash
git clone https://github.com/bhuvandereddy11/Morning-Briefing-.git
cd Morning-Briefing-
./install.sh
```

Then run it:

```bash
python3 wake_word_listener.py
```

Say **"good morning"** → your briefing plays. That's it.

---

## Configuration

Optionally create `~/.ok-claude.json` to customize:

```json
{
  "morning_words": ["good morning"],
  "cooldown_seconds": 30
}
```

| Option | Default | Description |
|---|---|---|
| `morning_words` | `["good morning"]` | Phrases that trigger the briefing |
| `cooldown_seconds` | `30` | Seconds before it can trigger again |

---

## Run on startup

1. Open **Script Editor** on your Mac
2. Paste this and save as an Application:

```applescript
do shell script "cd /path/to/Morning-Briefing- && python3 wake_word_listener.py &> /tmp/morning-briefing.log &"
```

3. Go to **System Settings → General → Login Items** and add the app.

---

## Privacy

- Uses **Google Speech Recognition** — audio snippets are sent to Google's API for transcription
- For fully offline recognition, swap in [Vosk](https://alphacephei.com/vosk/)

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

**Mic not working**
- Grant microphone access: System Settings → Privacy & Security → Microphone → Terminal

**Mishearing the trigger phrase**
- Adjust `recognizer.energy_threshold` in the script (lower = more sensitive)
- The trigger is any phrase containing "good morning" — keep it natural

---

## Project structure

```
Morning-Briefing-/
├── wake_word_listener.py   # main voice listener + morning briefing
├── config.example.json     # example config file
├── install.sh              # one-command installer
└── README.md
```

---

## License

MIT — do whatever you want with it.

---

*Built with Python + AppleScript + a little Claude magic*
