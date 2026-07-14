#!/bin/bash
# JSON Table Editor — Double-click to launch
cd "$(dirname "$0")"

# Kill any existing instance on the same port
lsof -ti:5050 2>/dev/null | xargs kill 2>/dev/null

# Start the server in background
python3 app_launcher.py &

# Wait a moment for the browser to open
sleep 2
