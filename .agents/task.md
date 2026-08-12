# Rental Operations Tasks & Implementation Plan

## Project Background & Module Overview 🚜

The **Rental Operations Module (Rental Desk)** is the central transaction engine of the **Apex Asset Operations Platform (AAOP)**. It binds registered business customers ([`Customer`](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/customer_model/customer.py)) to available machinery ([`BaseEquipment`](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/fleet_management_models/base_equipment.py) / [`PoweredEquipment`](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/fleet_management_models/powered_equipment.py)) through formal, immutable rental agreements ([`Contract`](file:///C:/Users/JoseMyrsonOBeros/PycharmProjects/EquipTrack/apex_asset_platform/models/contract.py)).

### Primary Objectives & Workflows to Build

1. **Equipment Dispatch Workflow (Issuing Contracts):**
   - Verify customer eligibility: Block customers flagged with an unpaid balance (`has_unpaid_balance == True`).
   - Verify machine availability: Block machinery marked `RENTED` or `IN_MAINTENANCE`.
   - Issue Contract: Lock starting engine run-hours (`initial_hours`), calculate base cost (`daily_rate * duration_days`), transition machine status to `RENTED`, and generate unique Contract ID tag (`CON-XXXX`).

2. **Equipment Return & Checkout Workflow:**
   - Record actual return metrics: Capture return date, current hour-meter reading (`return_hours`), and returned fuel levels.
   - Calculate Automated Surcharges & Penalties:
     - **Late Surcharge:** Standard daily rate + 50% penalty per overdue day.
     - **Refueling Penalty:** Missing fuel cost + flat $50 re-servicing fee.
   - Maintenance Auto-Flagging: If machine accumulated operating hours cross maintenance threshold (`current_hours - last_service_hours >= interval`), automatically transition status to `IN_MAINTENANCE`.
   - Update Customer Standing: If final return balance is unpaid, mark customer as `has_unpaid_balance = True`.
   - Restore Inventory: Return machine status to `AVAILABLE` (or `IN_MAINTENANCE`) and commit state changes to JSON disk storage (`contracts.json`, `fleet.json`, `customers.json`).

3. **Rental Desk Terminal Interface (`Interface/rental_desk_ui.py`):**
   - Interactive CLI sub-menu for dispatching equipment, processing returns, viewing active agreements, and searching contract receipts by ID.

---

## Workflow Rule: Strict Sequential Progression
> [!IMPORTANT]
> Tasks must be completed in order. Task N+1 remains locked until Task N is fully completed, clean, verified without errors, and documented with docstrings (`Args:` & `Returns:`).

---

## Task Status Summary

| Task | File Target | Status | Progression |
| :--- | :--- | :--- | :--- |
| **Task 1: Contract Domain Model** | `models/contract_model/contract.py` | `completed` | Finished |
| **Task 2: Rental Service Layer** | `services/rental_service.py` | `pending` | **[ACTIVE TASK]** |
| **Task 3: Rental Desk CLI Interface** | `Interface/rental_desk_ui.py` & `main.py` | `pending` | Locked |

---

## Task Details

### Task 1: Contract Domain Model (`Contract`) — `completed`
- **Target File:** `apex_asset_platform/models/contract_model/contract.py`
- **Status:** `completed`
- **Implemented Features:**
  - [x] Defined `Contract` domain entity class binding a customer and an equipment asset.
  - [x] Implemented attributes matching JSON schema: `contract_id` (str), `customer_id` (str), `asset_id` (str), `start_date` (str), `planned_end_date` (str), `actual_return_date` (str | None), `initial_hours` (float), `return_hours` (float | None), `fuel_at_dispatch_gal` (float), `fuel_returned_gal` (float | None), `daily_rate` (float), `base_cost` (float), `penalty_fees` (float), `status` (str - `ACTIVE`, `CLOSED`, `CANCELLED`).
  - [x] Implemented encapsulation via `@property` getters and setters with input boundary validation.
  - [x] Implemented `close_contract(actual_return_date, return_hours, fuel_returned_gal, fuel_fee_per_gal)` to calculate overdue days, refueling surcharges ($5/gal + $50 flat fee), update `penalty_fees`, and set status to `CLOSED`.
  - [x] Implemented `calculate_overdue_days(return_date_str) -> int` with fallback to `actual_return_date` or current date.
  - [x] Implemented `to_dict() -> dict` and `@classmethod from_dict(data: dict) -> Contract` with safe string float parsing.
  - [x] Implemented magic methods: `__repr__`, `__str__` (CLI formatting), `__eq__` (ID comparison).
  - [x] Included complete Google-style docstrings (`Args:` & `Returns:`).

---

### Task 2: Rental Service Layer (`RentalService`) — `completed`
- **Target File:** `apex_asset_platform/services/rental_service.py`
- **Status:** `completed`
- **Implemented Features:**
  - [x] Created `RentalService` class injected with `FleetService`, `CustomerService`, and `JSONRepository(Path("storage/contracts.json"))`.
  - [x] Implemented `_load_contract_cache()` and `_save_contract_cache()`.
  - [x] Implemented `create_contract(customer_id: str, asset_id: str, duration_days: int) -> Contract`:
    - [x] Check customer credit standing (`has_unpaid_balance == False`).
    - [x] Check equipment availability (`status == AVAILABLE`).
    - [x] Transition equipment state to `RENTED`.
    - [x] Generate unique Contract ID (`CNTR-XXXX`) with `validate_unique_ids` and save state to `contracts.json`.
  - [x] Implemented `process_return(contract_id: str, return_hours: float, fuel_returned_gal: float, date_returned: str, is_paid: bool) -> Contract`:
    - [x] Look up active contract and verify `status == "ACTIVE"`.
    - [x] Calculate penalties and close contract via `contract.close_contract(...)`.
    - [x] Check machine operating hours and auto-flag maintenance if interval exceeded (`requires_service()` $\rightarrow$ `IN_MAINTENANCE` vs `AVAILABLE`).
    - [x] Update customer delinquency standing if return balance is unpaid (`is_paid == False` $\rightarrow$ `flag_delinquent()`).
    - [x] Persist updated states to JSON storage files (`contracts.json`, `fleet.json`, `customers.json`).
  - [x] Implemented `get_active_contracts() -> list[Contract]` and `get_contract_by_id(contract_id: str) -> Contract`.
  - [x] Included complete Google-style docstrings (`Args:` & `Returns:`).

---

### Task 3: Rental Desk CLI Interface — `pending`
- **Target Files:** `apex_asset_platform/Interface/rental_desk_ui.py` & `apex_asset_platform/main.py`
- **Status:** `pending`
- **Required Features:**
  - [ ] Create interactive Rental Desk sub-menu (`display_rental_menu()`).
  - [ ] Connect CLI sub-options:
    - [ ] `1. Dispatch / Issue Rental Contract`
    - [ ] `2. Process Equipment Return & Checkout`
    - [ ] `3. View Active Rental Agreements`
    - [ ] `4. Search Contract by ID`
    - [ ] `5. Back to Main Menu`
  - [ ] Hook `RentalService` into `main.py` under main menu Option `3. Rental Desk (Dispatch & Return)`.
  - [ ] Handle input validation and display detailed billing summaries.
