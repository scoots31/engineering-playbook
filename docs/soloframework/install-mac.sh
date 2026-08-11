#!/bin/bash
# Solo Companion — Mac install
# Run with: curl -fsSL <url-to-this-file> | bash
set -e

REPO_URL="https://github.com/scoots31/solo-companion.git"
INSTALL_DIR="$HOME/Developer/Solo Companion"
PLIST_PATH="$HOME/Library/LaunchAgents/com.solocompanion.plist"
PORT=8710

echo "Installing Solo Companion..."

if ! command -v git >/dev/null 2>&1; then
    echo "Git is required. Install it from https://git-scm.com, then run this again."
    exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required. Install it from https://python.org, then run this again."
    exit 1
fi

mkdir -p "$HOME/Developer"

if [ -d "$INSTALL_DIR" ]; then
    echo "Found an existing install — updating it..."
    git -C "$INSTALL_DIR" pull
else
    echo "Downloading..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

if [ ! -d "$INSTALL_DIR/.venv" ]; then
    python3 -m venv "$INSTALL_DIR/.venv"
fi
"$INSTALL_DIR/.venv/bin/pip" install --quiet --upgrade pip flask

mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST_PATH" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.solocompanion</string>
    <key>ProgramArguments</key>
    <array>
        <string>$INSTALL_DIR/.venv/bin/python3</string>
        <string>$INSTALL_DIR/app.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$INSTALL_DIR/companion.log</string>
    <key>StandardErrorPath</key>
    <string>$INSTALL_DIR/companion.log</string>
</dict>
</plist>
PLIST

cat > "$HOME/Desktop/Solo Companion.webloc" <<WEBLOC
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>URL</key>
    <string>http://localhost:$PORT</string>
</dict>
</plist>
WEBLOC

launchctl unload "$PLIST_PATH" >/dev/null 2>&1 || true
launchctl load "$PLIST_PATH"

echo "Starting..."
for i in $(seq 1 15); do
    code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT" || true)
    if [ "$code" = "200" ]; then
        open "http://localhost:$PORT"
        echo ""
        echo "Solo Companion is running at http://localhost:$PORT"
        echo "It'll start automatically from now on — a shortcut is on your Desktop."
        echo "First launch will ask you to point it at the same folder you installed the Framework into."
        exit 0
    fi
    sleep 1
done

echo "Didn't start within 15 seconds — check $INSTALL_DIR/companion.log for what went wrong."
exit 1
