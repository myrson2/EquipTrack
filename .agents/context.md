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

---

### 11. Customer Accounts & Domain Architecture Implementation
- **Locations:**
  - [customer.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/customer_model/customer.py)
  - [customer_service.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/services/customer_service.py)
  - [customer_management_ui.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/Interface/customer_management_ui.py)
  - [validators.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/utils/validators.py)
  - [main.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/main.py)
- **Key Concepts & Features:**
  - **`Customer` Domain Model:** Created encapsulated domain model with `@property` getters and setters, dictionary serialization (`to_dict()`), factory constructor (`from_dict()` with safe string-boolean parsing), delinquency methods (`flag_delinquent()`, `clear_delinquent()`), and magic methods (`__repr__`, `__str__`, `__eq__`, `__lt__` for sorting by `customer_id`).
  - **`CustomerService` Layer:** Implemented service layer managing `storage/customers.json` via `JSONRepository`. Features `_load_customer_cache()`, `_save_customer_cache()`, `register_customer()` (with auto-generated `CUST-XXXX` IDs), `get_all_customers()`, `get_customer_by_id()`, `search_customers()`, and `update_credit_status()`.
  - **Validation Guardrails:** Created modular validator functions in `validators.py`: `gmail_validator()` (validates `@gmail.com`), `phone_validator()` (validates `09` prefix and 11-digit length), and safe `validate_unique_ids()` using `getattr()` to prevent `AttributeError` crashes across different domain model lists.
  - **CLI Sub-Menu Integration:** Created `display_customer_menu()` and `handle_customer_management()` in `customer_management_ui.py` for creating accounts, viewing registered accounts, and filtering accounts by status (`PAID` vs `UNPAID`). Connected to `main.py` Option `2. Customer Accounts`.

---

### 13. Persona Guidelines & Autocomplete Rule Refinements
- **Location:** [AGENTS.md](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/AGENTS.md#L83-L91)
- **Key Guideline Updates:**
  - **Strict Function Autocomplete Permission:** Added explicit exception rule: `__init__` and magic methods (`__repr__`, `__str__`, `__eq__`, `__lt__`) are fully autocompleted by default. All other unconfirmed domain/business logic methods remain as `pass` stubs to guide the user via the Socratic method.
  - **Senior Developer Architectural Insights & Tradeoffs:** Combined child-friendly real-world analogies with Senior Developer architectural tradeoff analysis (explaining *why* concepts are useful, pros vs. cons, and enterprise design patterns).

---

### 14. Contract Domain Model (`Contract`) Implementation
- **Location:** [contract.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/contract_model/contract.py)
- **Key Concepts & Features:**
  - **JSON Schema Alignment:** Defined 12 core attributes (`contract_id`, `customer_id`, `asset_id`, `start_date`, `planned_end_date`, `actual_return_date`, `initial_hours`, `return_hours`, `fuel_at_dispatch_gal`, `fuel_returned_gal`, `daily_rate`, `base_cost`, `penalty_fees`, `status`).
  - **Encapsulated `@property` Boundary Defenses:** Implemented getters and setters enforcing non-empty string ID checks, non-negative float validation for rates/hours/fees, and valid status state machine choices (`ACTIVE`, `CLOSED`, `CANCELLED`).
  - **Magic Methods:** Autocompleted `__init__`, `__repr__` (developer inspection), `__str__` (operator CLI summary formatting), and `__eq__` (equality by `contract_id`).

---

### 15. Rental Desk Operations & Checkout Workflow (`RentalService` & `rental_management_ui.py`)
- **Locations:**
  - [rental_service.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/services/rental_service.py)
  - [rental_management_ui.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/Interface/rental_management_ui.py)
- **Key Concepts & Features:**
  - **Dispatch Workflow (`create_contract`):** Validates customer credit standing (`has_unpaid_balance`), asset availability (`AVAILABLE`), binds IDs, generates `CNTR-XXXX` contract receipts, and transitions equipment status to `RENTED`.
  - **Return Checkout Workflow (`process_return`):** Accepts actual return date, meter run-hours, and returned fuel levels. Calculates pro-rated base costs, overdue late fees (1.5x daily rate), and refueling surcharges ($5.00/gal + $50 servicing fee). Automatically updates machinery run-hours, auto-flags `IN_MAINTENANCE` status via engine service thresholds (`requires_service()`), and flags customer accounts `UNPAID` / delinquent if return invoices remain unpaid.
  - **Interactive Rental Desk CLI Sub-Menu:** Built options 1 to 5 in `rental_management_ui.py` for dispatching contracts, processing return checkouts, listing active agreements, searching receipts by ID, and returning to the main menu.

---

### 16. Maintenance Log Domain Model (`MaintenanceLog`) Implementation
- **Location:** [maintenance_log.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/maintenance_model/maintenance_log.py)
- **Key Concepts & Features:**
  - **JSON Schema Alignment:** Defined 7 core attributes matching `storage/maintenance.json` (`maintenance_id`, `asset_id`, `service_date`, `description`, `cost`, `meter_hours_at_service`, `performed_by`).
  - **Encapsulated `@property` Boundary Defenses:** Implemented getters/setters with safe float/string type parsing and boundary validation.
  - **Serialization Methods:** Implemented `to_dict() -> dict` and `@classmethod from_dict(data: dict) -> MaintenanceLog` handling string float conversions.
  - **Magic Methods:** Autocompleted `__init__`, `__repr__` (debugging), `__str__` (CLI formatting), `__eq__` (ID comparison), and `__lt__` (chronological date sorting for service reports).

---

### 17. Service & Maintenance Operations Sub-Menu (`MaintenanceService` & `maintenance_management_ui.py`)
- **Locations:**
  - [maintenance_service.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/services/maintenance_service.py)
  - [fleet_service.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/services/fleet_service.py)
  - [maintenance_management_ui.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/Interface/maintenance_management_ui.py)
  - [main.py](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/main.py)
- **Key Concepts & Features:**
  - **`MaintenanceService` Layer:** Implemented `_load_maintenance_cache()`, `save_maintenance_cache()`, and `append_maintenance_log(maintenance_log)` for storage persistence in `storage/maintenance.json`.
  - **`FleetService` Maintenance Completion:** Updated `complete_maintenance(maintenance_log)` to reset run-hour meters (`hours_at_last_service = current_hours`) for powered equipment, restore status to `AVAILABLE`, save `fleet.json`, and delegate log appends to `MaintenanceService`.
  - **Interactive Service Operations CLI Sub-Menu:** Built options 1 to 5 in `maintenance_management_ui.py` for listing pending maintenance assets, completing repairs and restoring equipment to inventory, manually flagging assets for service, and viewing historical service logs. Hooked to `main.py` Option `4. Service & Maintenance Operations`.




