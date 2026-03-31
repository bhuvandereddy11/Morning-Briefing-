#!/bin/bash
# ok-claude — Quick Launcher (no voice, just run this script)
# Use this as a Raycast script or bind it to a keyboard shortcut.
#
# ── EDIT YOUR URLS BELOW ──────────────────────────────────────────────────────

BROWSER="Google Chrome"   # or: Safari, Firefox, Arc, Brave Browser

URLS=(
  "https://claude.ai/projects"
  "https://mail.google.com/mail/u/5/#inbox"
  "https://www.linkedin.com/feed/"
  "https://www.notion.so/3074a07ba3d080fb8bc6e4ec2eb5828d?v=3074a07ba3d0813a9fff000c89a7c20b"
)

# ─────────────────────────────────────────────────────────────────────────────

echo "🚀 Opening morning routine tabs in $BROWSER..."

osascript <<EOF
tell application "$BROWSER"
    activate
    set firstURL to true
    repeat with u in {$(printf '"%s",' "${URLS[@]}" | sed 's/,$//')}
        if firstURL then
            open location u
            set firstURL to false
        else
            tell window 1
                set newTab to make new tab with properties {URL:u}
            end tell
        end if
    end repeat
end tell
EOF

echo "✅ Done! ${#URLS[@]} tabs opened."
