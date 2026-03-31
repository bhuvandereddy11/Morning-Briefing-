#!/usr/bin/env python3
"""
ok-claude — Wake Word Listener
Say "hey claude good morning" → reads macOS notifications + iMessages aloud.
"""

import subprocess
import sys
import time
import json
import os
import threading

# ── CONFIG ─────────────────────────────────────────────────────────────────────

MORNING_WORDS = ["good morning"]  # triggers on any phrase containing "good morning"

COOLDOWN_SECONDS = 30  # long enough to cover the full briefing
LANGUAGE = "en-US"
MAX_NOTIFICATIONS = 10

CONFIG_FILE  = os.path.expanduser("~/.ok-claude.json")
is_speaking  = threading.Event()  # set while say() is running — blocks re-triggers

# ───────────────────────────────────────────────────────────────────────────────


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def say(text):
    print(f"🔊 {text}")
    is_speaking.set()
    subprocess.run(["say", text], check=False)
    is_speaking.clear()


def play_sound(success=True):
    sound = "Glass" if success else "Basso"
    subprocess.run(["afplay", f"/System/Library/Sounds/{sound}.aiff"], check=False)


# ── MAC NOTIFICATIONS ──────────────────────────────────────────────────────────

def get_mac_notifications():
    """Check badge counts for common apps via AppleScript."""
    apps = {
        "Messages":  "iMessage",
        "Mail":      "Mail",
        "Slack":     "Slack",
        "WhatsApp":  "WhatsApp",
        "Telegram":  "Telegram",
    }
    results = []
    for app, label in apps.items():
        script = f'''
        tell application "System Events"
            if exists process "{app}" then
                tell process "{app}"
                    try
                        set b to badge description of UI element 1 of list 1 of group 1 of menu bar item 1 of menu bar 2
                        return b
                    end try
                end tell
            end if
        end tell
        '''
        try:
            r = subprocess.run(["osascript", "-e", script],
                               capture_output=True, text=True, timeout=5)
            val = r.stdout.strip()
            if val and val != "missing value":
                results.append((label, val))
        except Exception:
            continue
    return results


def get_imessage_unread():
    """Return unread iMessage count via AppleScript."""
    script = 'tell application "Messages" to get unread count of (first service whose service type is iMessage)'
    result = subprocess.run(["osascript", "-e", script],
                            capture_output=True, text=True, timeout=5)
    if result.returncode == 0 and result.stdout.strip().isdigit():
        return int(result.stdout.strip())
    return None


# ── MORNING BRIEFING ───────────────────────────────────────────────────────────

def morning_briefing():
    threading.Thread(target=play_sound, args=(True,), daemon=True).start()
    say("Good morning! Getting your briefing.")

    # macOS app badges
    print("\n🔔 Checking app notifications...")
    notifications = get_mac_notifications()
    if not notifications:
        say("No app notifications found.")
    else:
        for label, badge in notifications:
            say(f"{label} has {badge} notification{'s' if badge != '1' else ''}.")

    # iMessages
    try:
        unread = get_imessage_unread()
        if unread is not None:
            if unread == 0:
                say("No unread iMessages.")
            else:
                say(f"You have {unread} unread iMessage{'s' if unread != 1 else ''}.")
    except Exception:
        pass

    say("That's your morning briefing. Have a great day!")
    print("\n✅ Morning briefing done!\n")


# ── MAIN LOOP ──────────────────────────────────────────────────────────────────

def check_dependencies():
    missing = []
    try:
        import speech_recognition  # noqa: F401
    except ImportError:
        missing.append("SpeechRecognition")
    try:
        import pyaudio  # noqa: F401
    except ImportError:
        missing.append("pyaudio")
    if missing:
        print("❌ Missing dependencies. Run:\n")
        print(f"   pip install {' '.join(missing)}\n")
        sys.exit(1)


def listen_loop(morning_words, cooldown):
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.6

    last_triggered = 0

    print("🎙️  ok-claude is listening...")
    print('   Morning trigger: "hey/hi claude good morning"')
    print("   Press Ctrl+C to stop\n")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✓ Calibrated to ambient noise. Ready!\n")

                while True:
                    try:
                        audio = recognizer.listen(source, timeout=None, phrase_time_limit=6)
                        text = recognizer.recognize_google(audio, language=LANGUAGE).lower()

                        now = time.time()
                        if now - last_triggered < cooldown:
                            print("⏳ Cooldown active, ignoring...")
                            continue

                        if is_speaking.is_set():
                            continue  # ignore mic while voice is playing

                        if any(trigger in text for trigger in morning_words):
                            last_triggered = now
                            print(f'\n🌅 Morning greeting detected: "{text}"')
                            threading.Thread(target=morning_briefing, daemon=True).start()
                        else:
                            print(f"   heard: {text}")

                    except sr.WaitTimeoutError:
                        pass
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"⚠️  Google Speech API error: {e}")
                        time.sleep(3)

        except OSError:
            print("⚠️  Mic error, reconnecting in 2 seconds...")
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n\n👋 ok-claude stopped. Have a great day!")
            sys.exit(0)


def main():
    check_dependencies()

    user_config   = load_config()
    morning_words = user_config.get("morning_words", MORNING_WORDS)
    cooldown      = user_config.get("cooldown_seconds", COOLDOWN_SECONDS)

    listen_loop(morning_words, cooldown)


if __name__ == "__main__":
    main()
