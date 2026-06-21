import subprocess
import requests
import time

# subprocess — запуск зовнішніх команд (CLI Ollama).
# requests — перевірка доступності API.
# time — затримка після запуску сервера.

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"

# Перевірка чи запущений Ollama
# Функція перевіряє, чи працює сервер Ollama.
# Вона робить:
    # requests.get(OLLAMA_URL, timeout=1)
    # якщо сервер відповідає → True
    # якщо ні (timeout або помилка) → False

def is_ollama_running():
    try:
        requests.get(OLLAMA_URL, timeout=1)
        return True
    except:
        return False

# Запускається процес: дається 2 секунди, щоб сервер встиг стартувати.

def start_ollama():
    subprocess.Popen(["ollama", "serve"])
    time.sleep(2)

# Перевірка наявності моделі

def ensure_model():
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if OLLAMA_MODEL not in result.stdout:
        subprocess.run(["ollama", "pull", OLLAMA_MODEL])
        
# завантажує модель при відсутності

def ensure_ollama_ready():
    if not is_ollama_running():
        start_ollama()
    ensure_model()
