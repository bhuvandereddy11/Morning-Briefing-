#!/bin/bash
# Required Parameters:
# @raycast.schemaVersion 1
# @raycast.title Ok Claude
# @raycast.mode silent
# @raycast.packageName ok-claude
#
# Optional Parameters:
# @raycast.icon 🚀
# @raycast.description Open your morning routine tabs

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../scripts" && pwd )"
bash "$SCRIPT_DIR/open_tabs.sh"
