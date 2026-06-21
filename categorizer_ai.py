
# Режим з інтеграцією LLM. Розбір буде проведено нижче по розділам.


# Імпортуються всі необхідні модулі:

# dataclass — для зручного зберігання результату.
# json — для роботи з JSON-відповідями.
# re — регулярні вирази.
# requests — відправлення HTTP-запиту до Ollama.
# typing.Any — універсальний тип.

from __future__ import annotations
from dataclasses import dataclass
import json
import re
from typing import Any
import requests

# Задаються параметри моделі:

# адреса локального сервера Ollama;
# назва моделі, яка буде виконувати класифікацію.

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"


# Створюється структура для результату класифікації.

# Вона містить:

# головну категорію;
# підкатегорію;
# впевненість моделі;
# метод класифікації.

@dataclass(frozen=True)
class AiLLMResult:
    main_category: str
    subcategory: str
    confidence: float
    method: str = "LLM_OPEN"


class LLMCategorizer:
    def __init__(self, model: str = OLLAMA_MODEL, url: str = OLLAMA_URL, timeout: int = 60, max_chars: int = 600):
        self.model = model
        self.url = url
        self.timeout = timeout
        self.max_chars = max_chars

# Попередня обробка тексту

# прибираються зайві пробіли;
# текст приводиться до одного стандартного формату.
# після нормалізації текст обрізається до максимально допустимої довжини (max_chars).
    @staticmethod
    def _normalize_text(text: str) -> str:
        return " ".join((text or "").split())

    def _truncate_text(self, text: str) -> str:
        text = self._normalize_text(text)
        return text[: self.max_chars]

# Поясення та інструкції для моделі - на інтуїтивно зрозумілій мові. (ПРОМПТ)
# Промпт містить:

# роль моделі (система категоризації файлів);
# завдання;
# правила створення категорій;
# вимоги до формату відповіді;
# приклади правильних категорій;
# сам текст документа в кінці.
    
    @staticmethod
    def _build_prompt(text: str) -> str:
        return f"""
You are a file categorization system.

Task:
Read the file text and determine:
1. main_category
2. subcategory
3. confidence

Rules:
- You may create categories yourself.
- Use clear, human-readable names.
- main_category: 1 or 2 words maximum.
- subcategory: 1 or 2 words maximum.
- Prefer broad, stable categories over overly narrow ones.
- Do NOT create long technical phrases as category names.
- If the file is unclear, use:
  main_category = "Misc"
  subcategory = "LowConfidence"
- Return ONLY valid JSON. No explanations. No text.
- Confidence must be a number from 0.0 to 1.0.

Examples of good main category names:
- IT
- Industry
- Military
- Finance
- Study
- RealEstate
- Medicine
- Psychology
- Travel
- Art
- Sport
- Business
- Transport
- Books
- Personal
- Science
- Media
- Energy
- Law
- Architecture

Examples of good subcategory names:
- Programming
- Databases
- Automation
- Equipment
- Reports
- Contracts
- Diagnostics
- Marketing
- Aviation
- Rent
- Labs
- Assignments
- Documentation
- Analysis
- Research
- Accounting
- Salary
- Manufacturing
- Design
- Electronics
- Networks
- Security
- Testing
- Development
- Management
- Guides
- Banking
- History

File text:
{text}
""".strip()


# Перевірка JSON
# LLM повинна повернути JSON
# якщо JSON взагалі відсутній — генерує помилку.
    
    @staticmethod
    def _safe_json_load(raw: str) -> dict[str, Any]:
        raw = raw.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        match = re.search(r"\{[\s\S]*}", raw)
        if match:
            return json.loads(match.group(0))

        raise ValueError("Model did not return valid JSON")


# Перевіряється правильність назв категорій.

# Наприклад модель могла повернути

# Computer Programming Development

# Метод:
    # прибирає зайві пробіли;
    # замінює "/"
    # залишає максимум два слова.

    @staticmethod
    def _clean_label(value: str, fallback: str) -> str:
        value = (value or "").strip()
        if not value:
            return fallback

        value = re.sub(r"\s+", " ", value)
        value = value.replace("/", " ")
        words = value.split()

        if not words:
            return fallback

        return " ".join(words[:2])

# Перевіряється поле confidence. Має бути лише у визначеному суворому форматі від 0.0 до 1.0
    
    @staticmethod
    def _clean_confidence(value: Any) -> float:
        try:
            conf = float(value)
        except (TypeError, ValueError):
            return 0.0

        if conf < 0.0:
            return 0.0
        if conf > 1.0:
            return 1.0
        return conf

# метод для основної класифікації, тут задаються оснонвні генеральні налаштування відповідей моделі. "temperature" та "num_predict".
    
    def categorize(self, text: str) -> tuple[str, float, str]:
        text = self._truncate_text(text)

        if not text:
            return "Misc/Empty", 0.0, "LLM_OPEN_EMPTY"

        payload = {
            "model": self.model,
            "prompt": self._build_prompt(text),
            "stream": False,
            "options": {
                "temperature": 0,
                "num_predict": 50,
            },
        }

# формування HTTP запиту(payload) через requests
        
        try:
            response = requests.post(self.url, json=payload, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            return "Misc/LLMError", 0.0, f"LLM_FAILED: {type(e).__name__}"

# формування відповіді, витягується текст відповіді, відбувається перевірка JSON та після усіх зчитувань, 
# корекції та правок - зчитуються всі необхідні поля та повертається фінальний результат
        
        
        data = response.json()
        raw_response = data.get("response", "").strip()

        try:
            parsed = self._safe_json_load(raw_response)
        except Exception:
            return "Misc/ParseError", 0.0, "LLM_BAD_JSON"
        main_category = self._clean_label(parsed.get("main_category"), "Misc")
        subcategory = self._clean_label(parsed.get("subcategory"), "LowConfidence")
        confidence = self._clean_confidence(parsed.get("confidence"))

        if confidence < 0.30:
            main_category = "Misc"
            subcategory = "LowConfidence"

        return f"{main_category}/{subcategory}", confidence, "LLM_OPEN"
