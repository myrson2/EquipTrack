import json
from pathlib import Path

class JSONRepository:
    """Repository for managing JSON file persistence operations."""

    def __init__(self, file_path: Path) -> None:
        """Initializes JSONRepository with target file path for persistence.

        Args:
            file_path (Path): Path object pointing to target JSON storage file.
        """
        self.file_path = file_path

    def load_all(self) -> list[dict]:
        """Loads and deserializes all records from the target JSON file.

        Returns:
            list[dict]: List of dictionary records, or an empty list if the file does not exist.
        """
        if not self.file_path.exists():
            return []

        with open(self.file_path, "r", encoding="utf-8") as json_file:
            load_file = json.load(json_file)
        return load_file

    def save_all(self, data: list[dict]) -> None:
        """Overwrites the target JSON file with formatted dictionary records.

        Args:
            data (list[dict]): List of dictionary records to serialize and save.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
