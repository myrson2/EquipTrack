# Session Context & Development Log

## Overview
This document records all key topics, architectural discussions, decisions, and code updates conducted during this session for the **Apex Asset Operations Platform (AAOP)**.

---

## Summary of Conducted Work & Discussions

### 1. Creation and Configuration of `AGENTS.md`
- **Objective:** Establish a structured `AGENTS.md` file based on project requirements in `overview.md`.
- **Key Guidelines Added:**
  - Layered Architecture rules (CLI Menu → Service Layer → Repository Layer → JSON Storage).
  - Built-in Python modules only requirement (`json`, `pathlib`, `datetime`, `uuid`, `abc`, `typing`).
  - **Persona & Interaction Guidelines:** Act as a Senior Python Developer using the Socratic Method.
  - **Boilerplate Rule:** Ask the user if a code request is for boilerplate/stub creation. If confirmed, generate directly; otherwise, use the Socratic Senior Developer persona.
  - **Concept Explanation Rule:** Describe Python concepts, their descriptions, and their purpose first before guiding the user to write code, avoiding unprompted direct code snippets.

---

### 2. Implementation of `JSONRepository` (`json_repository.py`)
- **Location:** [json_repository.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/repositories/json_repository.py)
- **Class Design & Responsibilities:**
  - `__init__(self, file_path: Path)`: Accepts and stores the target JSON file path (`self.file_path`).
  - `load_all(self) -> list[dict]`: Reads and parses JSON data from `self.file_path` into Python dictionaries. Discussed handling file opening (`open(..., "r", encoding="utf-8")`) and handling missing file edge cases gracefully.
  - `save_all(self, data: list[dict]) -> None`: Overwrites `self.file_path` with a formatted JSON array using `json.dump(data, f, indent=4)`.
  - `append_record(self, record: dict) -> None`: Loads existing records via `load_all()`, appends the single `record` to the list in memory, and writes back using `save_all()`.

---

### 3. Startup Data Seeding & CSV-to-JSON Pipeline
- **Topic:** Loading initial CSV data from `data_sample/` into JSON files under `storage/`.
- **Design Decisions & Concepts:**
  - **Batching vs. Single-Item Writes:** Evaluated performance between calling `append_record()` in a loop (which performs I/O for every row) vs. collecting rows into a `list[dict]` using `csv.DictReader` and calling `save_all()` once per file.
  - **File Stem Matching:** Used `Path.stem` (e.g. `contracts.csv` stem `"contracts"`) to map dynamically to `storage/contracts.json`.
  - **Debugging `PermissionError: [Errno 13]`:** Identified that `open()` was being called on a directory path (`data_sample`) instead of individual file paths (`item`). Fixed by switching line 30 in [main.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/main.py#L30) to `with item.open("r", encoding="utf-8") as f:`.
  - **Iterating Files:** Discussed the difference between `folder.glob("*.csv")` vs. `item.is_file() and item.suffix == ".csv"`.

---

### 4. Exceptions & Boundary Defenses
- **Topic:** Differentiating built-in Python exceptions from custom domain exceptions.
- **Key Concepts:**
  - Avoiding naming conflicts between built-in `FileNotFoundError` and custom exceptions in `custom_exceptions.py`.
  - Using `Path.exists()` for defensive path checking before attempting file I/O.
