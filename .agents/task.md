# Rental Operations Tasks & Implementation Plan

## Workflow Rule: Strict Sequential Progression
> [!IMPORTANT]
> Tasks must be completed in order. Task N+1 remains locked until Task N is fully completed, clean, verified without errors, and documented with docstrings (`Args:` & `Returns:`).

---

## Task Status Summary

| Task | File Target | Status | Progression |
| :--- | :--- | :--- | :--- |
| **Task 1: Contract Domain Model** | `models/contract.py` | `pending` | **[ACTIVE TASK]** |
| **Task 2: Rental Service Layer** | `services/rental_service.py` | `pending` | Locked |
| **Task 3: Rental Desk CLI Interface** | `Interface/rental_desk_ui.py` & `main.py` | `pending` | Locked |

---

## Task Details

### Task 1: Contract Domain Model (`Contract`) — `pending`
- **Target File:** `apex_asset_platform/models/contract.py`
- **Status:** `pending`
- **Required Features:**
  - [ ] Define `Contract` domain entity class binding a customer and an equipment asset.
  - [ ] Implement attributes: `contract_id` (str), `customer_id` (str), `asset_id` (str), `start_date` (datetime/str), `planned_end_date` (datetime/str), `actual_return_date` (datetime/str | None), `initial_hours` (float), `return_hours` (float | None), `base_cost` (float), `penalty_fees` (float), `status` (str - `ACTIVE`, `CLOSED`, `CANCELLED`).
  - [ ] Implement encapsulation via `@property` getters and setters with input validation.
  - [ ] Implement `close_contract(return_date, final_hours, fuel_returned, fuel_fee_per_gal)` to calculate overdue days, usage overages, refueling surcharges, and update contract standing.
  - [ ] Implement `calculate_overdue_days() -> int`.
  - [ ] Implement `to_dict() -> dict` and `@classmethod from_dict(data: dict) -> Contract`.
  - [ ] Implement magic methods: `__repr__`, `__str__`, `__eq__`.
  - [ ] Include complete Google-style docstrings (`Args:` & `Returns:`).

---

### Task 2: Rental Service Layer (`RentalService`) — `pending`
- **Target File:** `apex_asset_platform/services/rental_service.py`
- **Status:** `pending`
- **Required Features:**
  - [ ] Create `RentalService` class injected with `FleetService`, `CustomerService`, and `JSONRepository(Path("storage/contracts.json"))`.
  - [ ] Implement `_load_contract_cache()` and `_save_contract_cache()`.
  - [ ] Implement `create_contract(customer_id: str, asset_id: str, duration_days: int) -> Contract`:
    - Check customer credit standing (`has_unpaid_balance == False`).
    - Check equipment availability (`status == AVAILABLE`).
    - Transition equipment state to `RENTED`.
    - Generate unique Contract ID (`CON-XXXX`) and save state.
  - [ ] Implement `process_return(contract_id: str, return_hours: float, fuel_returned: float, return_date: str) -> Contract`:
    - Look up active contract.
    - Calculate penalties and close contract.
    - Check machine operating hours and auto-flag maintenance if interval exceeded.
    - Update customer delinquency standing if balance is unpaid.
    - Transition equipment status to `AVAILABLE` (or `IN_MAINTENANCE`).
    - Persist updated states to JSON storage files.
  - [ ] Implement `get_active_contracts() -> list[Contract]` and `get_contract_by_id(contract_id: str) -> Contract`.
  - [ ] Include complete Google-style docstrings (`Args:` & `Returns:`).

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
