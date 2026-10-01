#!/bin/sh
# Render tools/og.html to og.png (1200x630) with headless Chrome.
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
"$CHROME" --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=1200,630 \
  --virtual-time-budget=5000 --screenshot="$(pwd)/og.png" "file://$(pwd)/tools/og.html"
