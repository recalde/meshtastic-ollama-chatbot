# Meshtastic Ollama Chatbot 🤖📡

This project creates a local bridge between a Meshtastic node and an Ollama LLM running on your home server. It lets your Wi-Fi Meshtastic node act as a chatbot client, allowing you to have conversations over LoRa.

## 🧠 Features

- Local-only, secure chatbot bridge
- Per-node memory context
- Truncation and context windowing for short-message radios
- Easy to extend or run in LXC/docker

## 🛠️ Setup

### 1. Clone & Configure

```bash
git clone https://github.com/yourname/meshtastic-ollama-chatbot.git
cd meshtastic-ollama-chatbot
cp .env.example .env
```

Update `.env` with your Ollama IP.

### 2. Install in LXC container

Make sure the container has:

- Python 3.11+
- USB or serial access to the Meshtastic node
- Network access to Ollama

```bash
apt update && apt install -y python3-pip
pip install -r requirements.txt
python3 main.py
```

## 💬 Example

Message your Wi-Fi node and get a reply from Ollama through your local bot.

---

MIT License.
