import os
import time
import json
import requests
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.markup import escape
from threading import Lock
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion

# 🎛 Setup
console = Console()
load_dotenv()

# 🔧 Environment Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC_SUB = os.getenv("MQTT_TOPIC_SUB", "meshtastic/chatbot/request")
MQTT_TOPIC_PUB = os.getenv("MQTT_TOPIC_PUB", "meshtastic/chatbot/reply")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "meshtastic_bot")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
MAX_REPLY_LEN = int(os.getenv("MAX_REPLY_LEN", "240"))
CONTEXT_DEPTH = int(os.getenv("CONTEXT_DEPTH", "5"))
CONTEXT_FILE = os.getenv("CONTEXT_FILE", "/data/context.json")

# 📒 Shared Context State
CONTEXT = {}
LOCK = Lock()

# 🔁 Load chat memory from disk
def load_context():
    global CONTEXT
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, "r") as f:
            CONTEXT = json.load(f)
        console.print("🔁 [yellow]Loaded chat history from disk[/yellow]")
    else:
        console.print("📄 [blue]No existing context found, starting fresh[/blue]")

# 💾 Save chat memory to disk
def save_context():
    with LOCK:
        with open(CONTEXT_FILE, "w") as f:
            json.dump(CONTEXT, f, indent=2)

# 🧠 Generate a response from Ollama
def generate_response(node_id, message):
    with LOCK:
        history = CONTEXT.get(node_id, [])
        is_new = len(history) == 0
        history.append(f"User: {message}")
        prompt = "\n".join(history[-CONTEXT_DEPTH:]) + "\nBot:"
        CONTEXT[node_id] = history[-CONTEXT_DEPTH:]

    if is_new:
        console.print(f"👋 [cyan]New chat started with [bold]{node_id}[/bold][/cyan]")
    else:
        console.print(f"📨 [cyan]Message received from [bold]{node_id}[/bold][/cyan]")

    start = time.perf_counter()

    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })

    elapsed = time.perf_counter() - start
    reply = response.json().get("response", "").strip()

    with LOCK:
        CONTEXT[node_id].append(f"Bot: {reply}")
        save_context()

    console.print(f"🤖 [green]Response to {node_id}:[/green] {escape(reply[:60])}... ⏱️ {elapsed:.2f}s")
    return reply[:MAX_REPLY_LEN]

# 📡 MQTT Connect Handler
def on_connect(client, userdata, flags, rc, properties=None):
    console.print(f"✅ [bold green]Connected to MQTT broker[/bold green] (code {rc})")
    client.subscribe(MQTT_TOPIC_SUB)
    console.print(f"📡 [blue]Subscribed to topic:[/blue] {MQTT_TOPIC_SUB}")

# 📥 MQTT Message Handler
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        node_id = payload.get("node", "unknown")
        text = payload.get("text", "")
        console.print(f"[{node_id}] 📝 {escape(text)}")

        reply = generate_response(node_id, text)
        response_payload = {
            "node": node_id,
            "text": reply
        }
        client.publish(MQTT_TOPIC_PUB, json.dumps(response_payload))
        console.print(f"📤 [magenta]Reply sent to {node_id}[/magenta]")
    except Exception as e:
        console.print(f"[red]❌ Error processing message:[/red] {e}")

# 🚀 Start the chatbot
def main():
    load_context()
    client = mqtt.Client(client_id=MQTT_CLIENT_ID, callback_api_version=CallbackAPIVersion.V5)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    console.print("🚀 [bold green]Chatbot is live and listening...[/bold green]")
    client.loop_forever()

if __name__ == "__main__":
    main()