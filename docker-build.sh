#!/bin/bash

set -e

echo "🐳 Starting Docker build for Meshtastic Ollama Chatbot..."

# Optional --no-cache support
if [[ "$1" == "--no-cache" ]]; then
    echo "🧼 Building without cache..."
    docker build --no-cache -t meshtastic-chatbot .
else
    docker build -t meshtastic-chatbot .
fi

echo "✅ Build complete: [bold]meshtastic-chatbot:latest[/bold]"
echo "▶️  You can now run: docker-compose up -d"