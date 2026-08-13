# Apex Asset Operations Platform (AAOP) - Task Tracking & Maintenance Plan

## Project Overview 🚜

The **Maintenance & Service Operations Module** is the core operational health engine of the **Apex Asset Operations Platform (AAOP)**. It manages machinery maintenance lifecycles, tracks operating engine hours, auto-flags equipment exceeding service thresholds (`requires_service()`), processes mechanic service completions, and records permanent historical audit receipts in `storage/maintenance.json`.

---

## Workflow Rule: Strict Sequential Progression
> [!IMPORTANT]
> Tasks must be completed in order. Task N+1 remains locked until Task N is fully completed, clean, verified without errors, and documented with docstrings (`Args:` & `Returns:`).

---

## Task Status Summary

| Task | Target Component | Status | Progression |
| :--- | :--- | :--- | :--- |
| **Task 1: MaintenanceLog Domain Model** | `models/maintenance_model/maintenance_log.py` | `completed` | Finished |
| **Task 2: Fleet Service Maintenance Operations** | `services/fleet_service.py` | `pending` | **[ACTIVE TASK]** |
| **Task 3: Service Operations CLI Interface** | `Interface/service_operations_ui.py` & `main.py` | `pending` | Locked |

---

## Task Details

### Task 1: MaintenanceLog Domain Model (`MaintenanceLog`) — `completed`
- **Target File:** `apex_asset_platform/models/maintenance_model/maintenance_log.py`
- **Status:** `completed`
- **Implemented Features:**
  - [x] Defined `MaintenanceLog` domain entity class matching `storage/maintenance.json` schema (`maintenance_id`, `asset_id`, `service_date`, `description`, `cost`, `meter_hours_at_service`, `performed_by`).
  - [x] Implemented encapsulation via `@property` getters and setters with non-empty string and non-negative cost boundary validation.
  - [x] Implemented `to_dict() -> dict` and `@classmethod from_dict(data: dict) -> MaintenanceLog` with safe string float parsing.
  - [x] Implemented magic methods: `__repr__` (debugging), `__str__` (CLI formatting), `__eq__` (ID comparison), and `__lt__` (chronological date sorting).
  - [x] Included complete Google-style docstrings (`Args:` & `Returns:`).

---

### Task 2: Fleet Service Maintenance Operations (`FleetService`) — `pending`
- **Target File:** `apex_asset_platform/services/fleet_service.py`
- **Status:** `pending` (Active Progress)
- **Required Features:**
  - [ ] Implement `_load_maintenance_cache()` loading all historical records from `storage/maintenance.json`.
  - [ ] Implement `save_maintenance_cache()` serializing `MaintenanceLog` objects back to `storage/maintenance.json`.
  - [ ] Implement `flag_for_service(asset_id: str)`:
    - Sets `equipment.status = IN_MAINTENANCE`.
    - Immediately saves `storage/fleet.json` to lock asset from dispatch.
  - [ ] Implement `complete_maintenance(asset_id, description, cost, tech_name, service_date) -> MaintenanceLog`:
    - Resets `hours_at_last_service = current_hours` for `PoweredEquipment`.
    - Restores equipment status to `AVAILABLE`.
    - Generates unique `MNT-XXXX` log ID and appends `MaintenanceLog` to `maintenance_list`.
    - Saves updated states to both `storage/fleet.json` and `storage/maintenance.json`.
  - [ ] Implement `get_in_maintenance_equipment() -> list[BaseEquipment]` and `get_maintenance_logs_by_asset(asset_id: str) -> list[MaintenanceLog]`.

---

### Task 3: Service Operations CLI Interface — `pending`
- **Target Files:** `apex_asset_platform/Interface/service_operations_ui.py` & `apex_asset_platform/main.py`
- **Status:** `pending`
- **Required Features:**
  - [ ] Create interactive Service Operations sub-menu (`display_service_menu()`):
    - [ ] `1. View Equipment Pending Maintenance (IN_MAINTENANCE)`
    - [ ] `2. Complete Maintenance & Restore to Inventory (IN_MAINTENANCE -> AVAILABLE)`
    - [ ] `3. Manually Flag Equipment for Service (AVAILABLE -> IN_MAINTENANCE)`
    - [ ] `4. View Maintenance Logs & Service History`
    - [ ] `5. Back to Main Menu`
  - [ ] Hook `handle_service_operations(fleet_svc)` into `main.py` under main menu Option `4. Service & Maintenance Operations`.
