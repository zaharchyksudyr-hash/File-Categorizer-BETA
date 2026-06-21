import subprocess
import requests
import time

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"

def is_ollama_running():
    try:
        requests.get(OLLAMA_URL, timeout=1)
        return True
    except:
        return False

def start_ollama():
    subprocess.Popen(["ollama", "serve"])
    time.sleep(2)

def ensure_model():
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if OLLAMA_MODEL not in result.stdout:
        subprocess.run(["ollama", "pull", OLLAMA_MODEL])

def ensure_ollama_ready():
    if not is_ollama_running():
        start_ollama()
    ensure_model()