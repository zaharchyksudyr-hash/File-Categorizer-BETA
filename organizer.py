from pathlib import Path
import shutil
import re

from core.reporter import Reporter
from dataclasses import dataclass

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

@dataclass(frozen=True)
class MovePlanItem:
    source: Path
    category: str
    score: str = "-"
    method: str = "UNKNOWN"

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
        except Exception as e:
            reporter.log(mode,item,destination_file,category,status="ERROR",error=repr(e))

        if status_callback:
            status_callback(f"Applying: {item.name}")

        if progress_callback:
            progress_callback(int(index/total*100))

    return result