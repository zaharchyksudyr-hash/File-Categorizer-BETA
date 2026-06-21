# pathlib (Path) — використовується для створення папки з логами та динамічного формування безпечних шляхів до CSV-файлів незалежно від операційної системи.
# csv — вбудований модуль для роботи з табличними даними. Він автоматично екранує спецсимволи, розділяє змінні комами та формує правильну структуру CSV-файлу.
# datetime (datetime) — використовується для фіксації часу. 
# Застосовується двічі: для створення унікального імені файлу (.strftime) та для збереження точного часу кожної окремої операції у стандарті ISO (.isoformat).

from pathlib import Path
import csv
from datetime import datetime

class Reporter:

# При створенні об'єкта автоматично генерує нову папку для логів (за замовчуванням logs/) та створює унікальний CSV-файл, 
# ім'я якого містить поточну дату та час. Також він відразу записує рядок заголовків(headers).
    
    def __init__(self, log_folder: str = "logs") -> None:
        self.log_folder = Path(log_folder)
        self.log_folder.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_path = self.log_folder / f"operations_{timestamp}.csv"

        self.file = self.log_path.open("w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)

        headers = ["timestamp", "mode", "source", "destination", "category", "status", "error"]
        self.writer.writerow(headers)

# Записує новий рядок у CSV-файл із деталями операції:
# точний час, режим роботи, початковий та кінцевий шлях файлу, 
# категорію, статус (OK, SKIP, ERROR) та текст помилки, якщо вона виникла. 
# Виклик .flush() гарантує, що дані записуються на диск миттєво.
    
    def log(self, mode: str, source, destination, category: str, status: str = "OK", error: str = "") -> None:
        self.writer.writerow([
        datetime.now().isoformat(),
        str(mode),
        str(source),
        str(destination),
        str(category),
        str(status),
        str(error),])

        self.file.flush()

# Гарантують безпечне закриття файлу після завершення роботи програми, щоб уникнути витоку пам'яті чи пошкодження даних.
    
    def close(self) -> None:
        self.file.close()

    def __del__(self):
        try:
            self.file.close()
        except Exception:
            pass
