#!/bin/bash

echo "🛠️  Meshtastic ↔️ Ollama Chatbot Installer"
echo "----------------------------------------"

# Prompt for env variables
read -p "🔗 MQTT Broker address (e.g. mqtt or localhost): " mqtt_broker
read -p "📡 MQTT Port [1883]: " mqtt_port
mqtt_port=${mqtt_port:-1883}

read -p "📨 MQTT Subscribe Topic [meshtastic/chatbot/request]: " mqtt_sub
mqtt_sub=${mqtt_sub:-meshtastic/chatbot/request}

read -p "📤 MQTT Publish Topic [meshtastic/chatbot/reply]: " mqtt_pub
mqtt_pub=${mqtt_pub:-meshtastic/chatbot/reply}

read -p "🤖 MQTT Client ID [meshtastic_bot]: " mqtt_client
mqtt_client=${mqtt_client:-meshtastic_bot}

read -p "🌐 Ollama URL (e.g. http://host.docker.internal:11434): " ollama_url
read -p "💬 Ollama Model [llama3]: " ollama_model
ollama_model=${ollama_model:-llama3}

read -p "🧠 Max reply length [240]: " max_reply
max_reply=${max_reply:-240}

read -p "📚 Context memory depth [5]: " context_depth
context_depth=${context_depth:-5}

# Save to .env
cat <<EOF > .env
MQTT_BROKER=$mqtt_broker
MQTT_PORT=$mqtt_port
MQTT_TOPIC_SUB=$mqtt_sub
MQTT_TOPIC_PUB=$mqtt_pub
MQTT_CLIENT_ID=$mqtt_client

OLLAMA_URL=$ollama_url
OLLAMA_MODEL=$ollama_model
MAX_REPLY_LEN=$max_reply
CONTEXT_DEPTH=$context_depth
CONTEXT_FILE=/data/context.json
EOF

echo "✅ .env file created."

# Create Docker volume for context if not present
docker volume create chatbot_data >/dev/null 2>&1

# Build Docker container
echo "🐳 Building Docker container..."
docker-compose build

echo "✅ Docker build complete."
echo "▶️  Run with: docker-compose up -d"