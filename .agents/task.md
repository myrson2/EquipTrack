# Fleet Management Tasks & Implementation Plan

## Workflow Rule: Strict Sequential Progression
> [!IMPORTANT]
> Tasks must be completed in order. Task N+1 remains locked until Task N is fully completed, clean, verified without errors, and documented with docstrings (`Args:` & `Returns:`).

---

## Task Status Summary

| Task | File Target | Status | Progression |
| :--- | :--- | :--- | :--- |
| **Task 1: Base Equipment Model** | `models/fleet_management_models/base_equipment.py` | `completed` | Finished |
| **Task 2: Powered Equipment Subclass** | `models/fleet_management_models/powered_equipment.py` | `completed` | Finished |
| **Task 3: Fleet Service Orchestration** | `services/fleet_service.py` | `completed` | Finished |
| **Task 4: CLI Fleet Management Menu Base** | `main.py` | `completed` | Finished |
| **Task 5: Fleet Manager Enhancements** | `services/fleet_service.py` & `main.py` | `pending` | **[ACTIVE TASK]** |

---

## Task Details

### Task 1: Abstract Base Model `BaseEquipment` — `completed`
- **Target File:** `apex_asset_platform/models/fleet_management_models/base_equipment.py`
- **Status:** `completed`
- **Implemented Features:**
  - [x] Defined `BaseEquipment` class with attributes (`asset_id`, `model_name`, `daily_rate`, `purchase_year`, `status`).
  - [x] Implemented encapsulation via `@property` getters and setters with input boundary validation.
  - [x] Implemented `to_dict()` dictionary serialization.
  - [x] Implemented `calculate_rental_cost()`, `mark_maintenance()`, and `mark_available()`.
  - [x] Implemented magic methods (`__repr__`, `__str__`, `__eq__`, `__lt__` for sorting by `asset_id`).
  - [x] Added Google-style docstrings with `Args:` and `Returns:` for all methods/properties.

---

### Task 2: Specialized Subclass `PoweredEquipment` — `completed`
- **Target File:** `apex_asset_platform/models/fleet_management_models/powered_equipment.py`
- **Status:** `completed`
- **Implemented Features:**
  - [x] Inherited from `BaseEquipment`.
  - [x] Added powered-specific attributes (`current_hours`, `hours_at_last_service`, `service_interval_hours`, `fuel_capacity_gallons`, `current_fuel_gal`).
  - [x] Implemented getters and setters with validation rules for engine attributes.
  - [x] Overrode `to_dict()` using `super().to_dict()`.
  - [x] Implemented `record_usage(hours_added: float, fuel_remaining: float)` with tank capacity checks and hour accumulation.
  - [x] Implemented `requires_service() -> bool` threshold check.
  - [x] Implemented `calculate_rental_cost(days: int) -> float`.
  - [x] Added Google-style docstrings with `Args:` and `Returns:` for all methods/properties.

---

### Task 3: `FleetService` Layer Orchestration — `completed`
- **Target File:** `apex_asset_platform/services/fleet_service.py`
- **Status:** `completed`
- **Implemented Features:**
  - [x] **Constructor (`__init__`)**: Dependency injection of `JSONRepository`.
  - [x] **`_load_initial_fleet()`**: Deserializes raw JSON dicts into `PoweredEquipment` and `BaseEquipment` object instances in `self.equipment_list`.
  - [x] **`save_equipment_list_to_storage()`**: Serializes all objects back to JSON disk storage.
  - [x] **`add_equipment(equipment: BaseEquipment)`**: Intercepts duplicate IDs, appends to cache, and persists to disk.
  - [x] **`get_all_equipment()`**: Returns `sorted(self.equipment_list)`.
  - [x] **`get_available_assets()`**: Returns list of available equipment.
  - [x] **`get_equipment_by_id(asset_id: str)`**: Looks up asset by ID or raises ValueError.
  - [x] **`flag_for_service(asset_id: str)`**: Mutates status to maintenance and persists to disk.
  - [x] **`update_hours_and_check_service(...) -> bool`**: Updates run-hours & fuel, auto-flags maintenance, saves to disk, and returns boolean flag.
  - [x] Added Google-style docstrings with `Args:` and `Returns:` for all methods.

---

### Task 4: CLI Integration (Option 1 Menu Base) — `completed`
- **Target File:** `apex_asset_platform/main.py`
- **Status:** `completed`
- **Implemented Features:**
  - [x] Initialized `JSONRepository(Path("storage/fleet.json"))` and injected into `FleetService`.
  - [x] Created `display_fleet_menu()` with clean 2-space UI indentation.
  - [x] Connected CLI Option `1. Fleet Management` to interactive sub-menu handler.
  - [x] Added Google-style docstrings with `Args:` and `Returns:` for all CLI handlers.

---

### Task 5: Fleet Manager Enhancements (Filtering & Parameter Updates) — `pending` **[ACTIVE TASK]**
- **Target Files:** `apex_asset_platform/services/fleet_service.py` & `apex_asset_platform/main.py`
- **Status:** `pending`
- **Action Items to Implement:**
  - [ ] **Service Method `get_equipment_by_status(status: EquipmentStatus) -> list[BaseEquipment]`**: Filter inventory by any operational status (`AVAILABLE`, `IN_MAINTENANCE`, `RENTED`).
  - [ ] **Service Method `update_equipment_status(asset_id: str, new_status: EquipmentStatus) -> None`**: Manually toggle machine status and persist to JSON storage.
  - [ ] **Service Method `update_powered_parameters(...)`**: Modify engine hours, service intervals, tank capacities, or daily rates and persist to JSON storage.
  - [ ] **CLI Catalog Filter Expansion (Option 2 in `main.py`)**:
    - `1. All Fleet Assets`
    - `2. Available Assets`
    - `3. Assets In Maintenance`
    - `4. Rented Assets`
  - [ ] **CLI Parameter & Status Update Menu (Option 4 in `main.py`)**:
    - Add sub-option `4. Update Equipment Parameters & Status` in `display_fleet_menu()`.
    - Prompt for `Asset Tag ID` and allow modifying status, daily rates, run-hours, service intervals, or fuel tank capacity.
