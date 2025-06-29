#!/bin/bash

# Percorso allo script Python
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/fetch_scoreboard.py"

# Loop infinito ogni 60 secondi
while true; do
    echo "Esecuzione fetch_scoreboard.py alle $(date)"
    python3 "$SCRIPT_PATH"
    echo "In attesa 60 secondi..."
    sleep 60
done
