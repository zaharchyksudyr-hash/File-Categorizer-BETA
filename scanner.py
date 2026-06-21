from pathlib import Path

def folder_way(folder_path: str, exclude_folder: set[str] | None = None) -> list:
    folder = Path(folder_path)
    result: list[Path] = []

    if not folder.exists():
        print(folder_path, "Error: chosen folder does not exist")
        return result

    if not folder.is_dir():
        print(folder_path, "Error: selected variant is not a folder")
        return result

    for extension in (".txt", ".docx", ".pdf", ".md", ".xlsx", ".pptx"):
        for item in folder.rglob(f"*{extension}"):
            if not item.is_file():
                continue
            if any(part in exclude_folder for part in item.parts):
                continue
            if item.name.startswith("~$"):
                continue
            result.append(item)

    return result