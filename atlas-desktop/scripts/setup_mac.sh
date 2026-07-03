#!/usr/bin/env bash
# Atlas Desktop — one-time macOS setup.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "▶ Atlas Desktop setup (macOS)"

# 1. System audio dependency for sounddevice/PortAudio
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. Install from https://brew.sh then re-run." >&2
  exit 1
fi
echo "▶ Installing PortAudio (audio I/O)…"
brew list portaudio >/dev/null 2>&1 || brew install portaudio

# 2. Python virtual environment
if [ ! -d ".venv" ]; then
  echo "▶ Creating Python venv…"
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
echo "▶ Installing Python dependencies…"
pip install --upgrade pip
pip install -r requirements.txt

# 3. Secrets file
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "▶ Created .env — open it and fill in your keys before running."
fi

# 4. Node / Claude Code CLI (the Agent SDK shells out to it)
if ! command -v claude >/dev/null 2>&1; then
  echo "⚠ 'claude' CLI not found. The Agent SDK needs it. Install:"
  echo "    npm install -g @anthropic-ai/claude-code"
fi

mkdir -p keywords
cat <<'EOF'

✔ Setup complete.

Next:
  1. Fill in atlas-desktop/.env         (Anthropic, Google Cloud, Picovoice keys)
  2. Make your "Hey Atlas" wake word     (see scripts/get_wakeword.md) → keywords/
  3. Run it:
        source .venv/bin/activate
        python -m atlas_voice.main

Then just say:  "Hey Atlas, what's on my schedule today?"
EOF
