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

---

### 5. Implementation of Domain Entity Models (`BaseEquipment` & `PoweredEquipment`)
- **Location:**
  - [base_equipment.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/fleet_management_models/base_equipment.py)
  - [powered_equipment.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/fleet_management_models/powered_equipment.py)
  - [enum.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/fleet_management_models/enum.py)
- **Key Concepts & Design:**
  - **`BaseEquipment`**: Serves as the domain entity base class with properties `asset_id`, `model_name`, `daily_rate`, `purchase_year`, and `status`. Uses `@property` decorators for encapsulated validation. Includes rental cost calculation, maintenance status transitions (`mark_maintenance()`, `mark_available()`), dictionary serialization (`to_dict()`), and standard magic methods (`__repr__`, `__str__`, `__eq__`, `__lt__`).
  - **`PoweredEquipment`**: Inherits from `BaseEquipment` and adds engine operational state attributes (`current_hours`, `hours_at_last_service`, `service_interval_hours`, `fuel_capacity_gallons`, `current_fuel_gal`). Overrides `to_dict()` and `calculate_rental_cost()` (incorporating operating hour surcharges), and provides logic for usage logging (`record_usage()`) and service threshold evaluation (`requires_service()`).
  - **`EquipmentStatus` & `EquipmentType` Enums**: Encapsulate status (`AVAILABLE`, `RENTED`, `IN_MAINTENANCE`) and equipment categorization (`BASE`, `POWERED`).

---

### 6. Implementation of `FleetService` Layer Orchestration
- **Location:** [fleet_service.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/services/fleet_service.py)
- **Key Concepts & Responsibilities:**
  - **Dependency Injection:** Accepts `JSONRepository` in `__init__()` and maintains an in-memory cache list `equipment_list`.
  - **Deserialization (`_load_initial_fleet()`)**: Converts raw dictionary data from JSON disk storage into `PoweredEquipment` or `BaseEquipment` model instances.
  - **Fleet Operations:** Implements CRUD & business logic methods including `add_equipment()`, `get_all_equipment()`, `get_available_assets()`, `get_equipment_by_id()`, `flag_for_service()`, and `update_hours_and_check_service()` with auto-flagging for maintenance when threshold standard hours are exceeded.
  - **Persistence:** Synchronizes in-memory object list back to JSON file storage via `save_equipment_list_to_storage()`.

---

### 7. CLI Fleet Management Menu Integration
- **Location:**
  - [fleet_management_ui.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/Interface/fleet_management_ui.py)
  - [main.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/main.py)
- **Key Concepts & Features:**
  - **UI Decoupling:** Modularized terminal UI operations into `FleetManagementUI` class inside `Interface/fleet_management_ui.py`.
  - **Menu Handlers:** Provides interactive sub-options for viewing fleet catalog, registering new equipment, recording usage hours & fuel levels for powered assets, and flagging machinery for maintenance.
  - **`main.py` Integration:** Connects menu option `1. Fleet Management` directly to `FleetManagementUI.display_fleet_menu()`.

---

### 8. Structural Pattern Matching Refactoring & Docstring Standardization
- **Locations:**
  - [fleet_management_ui.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/Interface/fleet_management_ui.py#L82-L103)
  - [json_repository.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/repositories/json_repository.py)
- **Key Concepts & Changes:**
  - **Match-Case Refactoring:** Refactored binary `if-else` filter choices into Python 3.10+ `match filter_choice:` pattern matching.
  - **Expanded Options [1-5]:** Added sub-menu options for `1. All Fleet Assets`, `2. Available Assets Only`, `3. Assets in Maintenance`, `4. Rented Assets`, and `5. Back to Main Menu`.
  - **Safety & Stubs:** Initialized `assets = []` defensive list default, added `pass` stubs for cases `"3"` and `"4"` (pending `get_equipment_by_status` service layer implementation), and added wildcard `case _:` fallback for invalid inputs.
  - **Docstring Completeness:** Added Google-style docstrings (`Args:` and `Returns:`) across all methods in `JSONRepository` (`__init__`, `load_all`, `save_all`, `append_record`).

---

### 9. Maintenance Status Transition & Catalog Filter Integration
- **Locations:**
  - [fleet_service.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/services/fleet_service.py#L89-L166)
  - [fleet_management_ui.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/Interface/fleet_management_ui.py#L18-L69)
- **Key Concepts & Features:**
  - **Status Filtering:** Added `get_in_maintenance_equipment()` and `get_rented_equipment()` methods to `FleetService`.
  - **Maintenance Completion Workflow:** Implemented `update_equipment_status(fleet_item)` to reset `hours_at_last_service = current_hours` for powered machinery and transition status to `AVAILABLE` if service requirements are met.
  - **Interactive CLI Catalog Section:** Extracted catalog choices into `fleet_catalog_section(fleet_svc)`, connecting options 3 and 4 directly to service filter queries, and allowing operators to interactively select items from the maintenance list to update back to `AVAILABLE`.

---

### 10. Model Inheritance Fix & Maintenance Status Refinement
- **Locations:**
  - [powered_equipment.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/fleet_management_models/powered_equipment.py#L40-L45)
  - [fleet_service.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/services/fleet_service.py#L32-L52)
- **Key Concepts & Fixes:**
  - **`asset_id` Propagation in Inheritance:** Updated `PoweredEquipment` constructor to pass `asset_id` up to `super().__init__(..., asset_id=asset_id)`, ensuring `asset_id` is preserved when loading records from disk or creating powered assets.
  - **`_load_initial_fleet` Deserialization:** Included `asset_id=record.get("asset_id")` in `_load_initial_fleet()` deserialization for both `PoweredEquipment` and `BaseEquipment`.
  - **Universal Maintenance Status Restoration:** Refined `update_equipment_status()` in `FleetService` to mark any equipment (static or powered) as `AVAILABLE`, while selectively updating `hours_at_last_service = current_hours` for powered machines.


