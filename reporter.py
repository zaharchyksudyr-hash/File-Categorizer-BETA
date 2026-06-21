from pathlib import Path
import csv
from datetime import datetime

class Reporter:

    def __init__(self, log_folder: str = "logs") -> None:
        self.log_folder = Path(log_folder)
        self.log_folder.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_path = self.log_folder / f"operations_{timestamp}.csv"

        self.file = self.log_path.open("w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)

        headers = ["timestamp", "mode", "source", "destination", "category", "status", "error"]
        self.writer.writerow(headers)

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

    def close(self) -> None:
        self.file.close()

    def __del__(self):
        try:
            self.file.close()
        except Exception:
            pass