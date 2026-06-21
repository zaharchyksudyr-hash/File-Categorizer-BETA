# Цей файл містить функцію folder_way, яка виконує глибокий рекурсивний пошук документів у вказаній директорії за заданими розширеннями та з урахуванням правил ігнорування.

from pathlib import Path

def folder_way(folder_path: str, exclude_folder: set[str] | None = None) -> list:
    folder = Path(folder_path)
    result: list[Path] = []
    
# Перевіряє, чи існує вказана папка та чи є вона директорією (а не файлом). Якщо ні — виводить помилку.
    if not folder.exists():
        print(folder_path, "Error: chosen folder does not exist")
        return result

    if not folder.is_dir():
        print(folder_path, "Error: selected variant is not a folder")
        return result

# За допомогою методу .rglob() сканує головну папку та всі її підпапки на наявність документів (.txt, .docx, .pdf, .md, .xlsx, .pptx).
    
    for extension in (".txt", ".docx", ".pdf", ".md", ".xlsx", ".pptx"):
        for item in folder.rglob(f"*{extension}"):
            if not item.is_file():
                continue

    # Пропускає файли, якщо:
    # Вони є системними/тимчасовими (назва починається з ~$, характерно для MS Office).
    # Будь-яка частина їхнього шляху міститься у списку виключень exclude_folder (наприклад, можна ігнорувати archive).
            
            if any(part in exclude_folder for part in item.parts):
                continue
            if item.name.startswith("~$"):
                continue
            result.append(item)

    return result
