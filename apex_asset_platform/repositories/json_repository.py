import json
from pathlib import Path

class JSONRepository:
    """Repository for managing JSON file persistence operations."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load_all(self) -> list[dict]:
        if not self.file_path.exists():
            return []

        with open(self.file_path, "r", encoding="utf-8") as json_file:
            load_file = json.load(json_file)
        return load_file

    def save_all(self, data: list[dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def append_record(self, record: dict) -> None:
        pass
