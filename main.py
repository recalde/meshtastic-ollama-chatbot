import os
import meshtastic
import meshtastic.serial_interface
import requests
import time
from meshtastic.mesh_pb2 import Data
from rich import print
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "llama3")
MAX_REPLY_LEN = int(os.getenv("MAX_REPLY_LEN", "240"))
CONTEXT_DEPTH = int(os.getenv("CONTEXT_DEPTH", "5"))

CONTEXT = {}

def generate_response(node_id, message):
    history = CONTEXT.get(node_id, [])
    history.append(f"User: {message}")
    prompt = "\n".join(history[-CONTEXT_DEPTH:]) + "\nBot:"
    CONTEXT[node_id] = history[-CONTEXT_DEPTH:]

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    reply = response.json().get("response", "").strip()
    CONTEXT[node_id].append(f"Bot: {reply}")
    return reply[:MAX_REPLY_LEN]

def on_receive(packet, interface):
    try:
        node = packet["from"]
        text = packet["decoded"]["text"]
        print(f"[{node}] {text}")

        reply = generate_response(node, text)
        interface.sendText(reply, destinationId=node)
    except Exception as e:
        print(f"[red]Error:[/red] {e}")

def main():
    iface = meshtastic.serial_interface.SerialInterface()
    iface.onReceive = lambda packet: on_receive(packet, iface)
    print("[green]Bot is listening...[/green]")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
