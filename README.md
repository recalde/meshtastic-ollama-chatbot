# 🤖 Meshtastic Ollama Chatbot

This project connects your **Meshtastic radio network** to an **Ollama LLM** (like LLaMA 3 or Claude) running locally. Chat messages from Meshtastic are forwarded via MQTT, processed with memory-aware prompts, and replies are sent back to the original sender.

---

## 🔧 Features

- 🧠 Per-radio conversation memory (context-aware)
- 💾 Persistent chat history stored to disk
- 📡 MQTT-based message relay (integrates easily with Home Assistant)
- ⏱️ Logs response time from Ollama per interaction
- 🤖 Emoji-rich console logs with new user detection

---

## 🚀 Quick Start

### 1. Clone the repo and build



```bash
git clone https://github.com/recalde/meshtastic-ollama-chatbot.git
cd meshtastic-ollama-chatbot
cp .env.example .env
docker-compose up --build -d
