
# Цей файл відповідає за фізичне сортування файлів по категоріях (підпапках) на основі заданих правил, із підтримкою уникнення дублікатів та логуванням.

# pathlib (Path) — сучасний інструмент для роботи з файловою системою. 
# Замінює модуль os.path, дозволяючи працювати зі шляхами до файлів 
# автоматично враховуює особливості різних ОС (Windows/Linux).

# shutil — модуль для високорівневих операцій над файлами. У коді використовуються:
    # shutil.copy2 — копіює файл разом із його метаданими (дата створення, права доступу).
    # shutil.move — безпечно переміщує або перейменовує файли та папки.

# re — модуль для роботи з регулярними виразами. 
# Використовується для пошуку та видалення старих числових індексів наприкінці файлу, 
# щоб уникнути накопичення зациклених копій (наприклад, перетворює file_1_1.txt назад у file).

# dataclasses (dataclass) — декоратор, який автоматично генерує спеціальні методи для класів, що зберігають дані. 
# Прапорець frozen=True робить об'єкт незмінним (read-only), що захищає дані від випадкових модифікацій під час роботи програми.


from pathlib import Path
import shutil
import re

from core.reporter import Reporter
from dataclasses import dataclass

# Функція захисту від перезапису файлів. Якщо файл із таким ім'ям уже існує в цільовій папці, 
# вона автоматично додає числовий індекс (наприклад, file_1.txt, file_2.txt)

def make_unique_name(destination_files: Path) -> Path:
    suffix = destination_files.suffix
    parent = destination_files.parent

    base_stem = re.sub(r"_\d+$", "", destination_files.stem)

    duplicate = parent / f"{base_stem}{suffix}"
    if not duplicate.exists():
        return duplicate

    counter = 1
    while True:
        duplicate = parent / f"{base_stem}_{counter}{suffix}"
        if not duplicate.exists():
            return duplicate
        counter += 1

# Незмінний дата-клас, що описує завдання для кожного файлу: звідки взяти (source), до якої категорії віднести (category) та додаткові метадані.

@dataclass(frozen=True)
class MovePlanItem:
    source: Path
    category: str
    score: str = "-"
    method: str = "UNKNOWN"


# Головна функція сортування. Вона приймає список файлів, створює потрібну структуру папок та обробляє файли у трьох режимах (mode):
    # preview — тільки симуляція та перевірка (без фізичних змін).
    # copy — копіювання файлів у нові папки за допомогою shutil.copy2.
    # move — повне переміщення файлів за допомогою shutil.move.

def organizer_sorted_folders(new_folder: str, files_rules: list[MovePlanItem], mode:str, progress_callback=None, status_callback=None) -> list:
    mainfolder = Path(new_folder)
    result: list[Path] = []
    mainfolder.mkdir(parents=True, exist_ok=True)
    reporter = Reporter()

    total = len(files_rules) if files_rules else 1

    for index, item_rules in enumerate(files_rules, start=1):
        item = item_rules.source
        category = item_rules.category or "UNKNOWN"

        sorted_subfolder = mainfolder / category
        sorted_subfolder.mkdir(parents=True, exist_ok=True)

        if not item.exists():
            reporter.log(mode, item, "", category, status="SKIP", error="File does not exist")
            if progress_callback:
                progress_callback(int(index/total*100))
            continue

        destination_file = make_unique_name(sorted_subfolder / item.name)

        try:
            match mode:
                case "preview":
                    reporter.log(mode, item, destination_file, category, status="OK")
                case "copy":
                    shutil.copy2(item, destination_file)
                    reporter.log(mode, item, destination_file, category, status="OK")
                    result.append(destination_file)
                case "move":
                    shutil.move(item, destination_file)
                    reporter.log(mode, item, destination_file, category, status="OK")
                    result.append(destination_file)
                case _:
                    raise ValueError(f"Unknown mode: {mode}")

        # Використовує клас Reporter для запису результату кожної операції.
        
        except Exception as e:
            reporter.log(mode,item,destination_file,category,status="ERROR",error=repr(e))

# Підтримує progress_callback та status_callback для відстеження прогресу (зручно для інтеграції з GUI-прогресбаром).
        
        if status_callback:
            status_callback(f"Applying: {item.name}")

        if progress_callback:
            progress_callback(int(index/total*100))

    return result
