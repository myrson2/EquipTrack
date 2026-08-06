# Client Project Brief: Equipment Rental & Asset Operations Platform

**Client Name:** Apex Field Systems Ltd.

**Project Lead:** Marcus Vance (VP of Operations)

**Target Delivery Window:** 1–2 Weeks (Estimated Core Build: 4–6 Hours)

---

# 1. Client Request

### Client Message

> "Hello,
> I ran across your consulting profile and wanted to reach out. I manage Apex Field Systems. We rent heavy industrial equipment—generators, commercial dehumidifiers, trenchers, earthmovers, and mobile lighting rigs—to mid-sized construction firms and utility subcontractors.
> Right now, our yard operations are a mess. We manage a fleet of roughly 120 high-value assets across two yards using three shared Google Sheets and a whiteboard in the dispatch office.
> Here is what keeps happening:
> 1. A customer calls to rent a 100kW diesel generator for three days. Dispatch sees it as 'Available' on the sheet, accepts the contract, and collects payment. But when the driver goes to load it, the generator is sitting in the shop with a blown head gasket because the service tech forgot to update the status.
> 2. Customers are returning equipment late or with empty fuel tanks, and our counter team forgets to assess penalty charges or fuel surcharge fees because the math has to be calculated manually every time.
> 3. We have zero audit trails on equipment maintenance history. When a machine breaks down on a job site, we can't tell whether it was due for a service interval or if the client abused it.
> 
> 
> We don't need a fancy cloud web portal or a mobile app right now. What we *do* need is a local, rock-solid CLI application that our dispatch operators and yard technicians can run directly on the front-desk terminal.
> It needs to handle our inventory, manage customer rentals, calculate fees with strict business rules, log maintenance actions, and save everything persistently so the desk terminal can be shut down at night without losing state.
> We have a budget set aside for this scope. If this terminal app runs reliably, we will contract you for Phase 2 later this year."

---

# 2. Project Overview

The **Apex Asset Operations Platform (AAOP)** is a terminal-based internal management system. It acts as a single point of operational control for tracking heavy machinery, managing rental lifecycles (reservation, dispatch, return, invoicing), enforcing maintenance cycles based on machine run-hours, and persisting operational logs across system restarts.

---

# 3. Functional Requirements

### Asset & Fleet Management

* **Register Equipment:** Add new machinery into the fleet catalog with specific types, operational rates, and maintenance threshold metrics.
* **Search & Inspect Inventory:** Search assets by unique ID, category, or current operational status.
* **Status Updates:** Transition assets manually between state flags (`AVAILABLE`, `RENTED`, `IN_MAINTENANCE`, `RETIRED`).

### Customer & Account Management

* **Register Customer:** Store business contact profiles, tax IDs, and credit status flags.
* **Search Customer:** Query account records and view historical rental logs.

### Rental Transaction Lifecycle

* **Create Rental Contract:** Issue a rental agreement binding a customer to one or more available equipment units for a defined duration.
* **Process Return:** Record equipment return date, current hour-meter reading, and returned fuel level; automatically calculate overdue penalties, usage overage fees, and refueling charges.
* **Cancel Reservation:** Cancel pending reservations and return reserved assets to the active pool.

### Maintenance & Service Tracking

* **Log Service Activity:** Record routine service events, emergency repairs, and costs against specific assets.
* **Flag Maintenance Needs:** Automatically mark assets as `IN_MAINTENANCE` when their accumulated operating hours cross service intervals.

### Reporting & Analytics

* **Revenue Summary:** Output financial metrics across specified date ranges (base rentals vs. penalty fee breakdowns).
* **Fleet Utilization Report:** Display total active hours, downtime percentage, and current status counts across all fleet categories.

---

# 4. Business Rules

1. **Asset Uniqueness:** Every piece of equipment must possess an immutable, unique Asset Tag ID (e.g., `EQ-1004`).
2. **State Transition Locks:** An asset marked as `RENTED` or `IN_MAINTENANCE` cannot be assigned to a new rental contract under any circumstances.
3. **Credit Verification:** Customers flagged with an `UNPAID_BALANCE` status or an inactive profile cannot initiate new rental contracts.
4. **Maintenance Threshold Enforcement:** Every asset category has a maximum operating hour threshold between service intervals (e.g., Heavy Excavators require service every 100 hours). Upon return, if `current_hours - last_service_hours >= interval`, the asset state MUST automatically transition to `IN_MAINTENANCE`.
5. **Fuel Surcharge Rules:** If an asset is returned with less fuel than dispatched, a fixed fee per gallon/liter missing is automatically assessed, plus a flat $50 re-servicing penalty fee.
6. **Overdue Penalty Scaling:** Late returns accrue the standard daily rate plus a 50% late-penalty surcharge for every day beyond the agreed contract end date.
7. **Negative Values Prohibited:** Meter hours, rental days, daily rates, and fuel levels can never be negative values.
8. **Immutable Completed Contracts:** Once a contract status reaches `CLOSED`, its financial totals, return metrics, and associated line items can no longer be edited or deleted.

---

# 5. Required OOP Concepts

Your design must naturally incorporate and demonstrate the following core concepts:

* **Classes & Objects:** Domain model representation (`Asset`, `Customer`, `Contract`).
* **Encapsulation:** Protected internal states (e.g., hours, balances) accessible and mutated strictly via validated public methods.
* **Inheritance:** Base class `Equipment` extended by specialized classes (e.g., `PoweredEquipment`, `StaticEquipment`) with category-specific attributes and behavior.
* **Polymorphism & Method Overriding:** Custom rate calculations or inspection procedures implemented differently across equipment subclasses.
* **Class Methods:** Factory constructors for instantiating models directly from JSON records or generating predefined object configurations.
* **Static Methods:** Pure helper utilities for financial calculations, date formatting, or validation routines.
* **Magic Methods:** Structural object string representations (`__repr__`, `__str__`), equality checks (`__eq__`), and value comparisons (`__lt__` for sorting assets by runtime or ID).
* **Exception Handling:** Robust boundary defenses using domain-specific exception structures.

---

# 6. Suggested Project Structure

```text
apex_asset_platform/
│
├── main.py                     # Application entry point & CLI loop
│
├── models/                     # Core domain entities
│   ├── __init__.py
│   ├── base_equipment.py       # Abstract/Base Equipment class
│   ├── equipment_types.py      # Inherited specialized equipment models
│   ├── customer.py             # Customer profile domain model
│   ├── contract.py             # Rental agreement & line-item models
│   └── maintenance_log.py      # Service event record model
│
├── services/                   # Business logic orchestration layer
│   ├── __init__.py
│   ├── fleet_service.py        # Fleet management & state logic
│   ├── rental_service.py       # Rental lifecycle & billing calculations
│   └── report_service.py       # Analytical summaries and metrics
│
├── repositories/               # Data access layer
│   ├── __init__.py
│   └── json_repository.py      # File reading, writing, and updating operations
│
├── exceptions/                 # Custom error definitions
│   ├── __init__.py
│   └── custom_exceptions.py
│
├── utils/                      # Helper modules
│   ├── __init__.py
│   ├── validators.py           # User input & format validation routines
│   └── formatters.py           # CLI table formatting & currency display
│
└── storage/                    # Persistent storage directory
    ├── fleet.json              # Equipment catalog records
    ├── customers.json          # Customer account records
    ├── contracts.json          # Rental history & contract records
    └── maintenance.json        # Service event logs

```

---

# 7. Required Classes

### Class: `Equipment` (Base / Abstract Model)

* **Purpose:** Represents generic operational characteristics common to all fleet inventory items.
* **Responsibilities:** Stores base metadata, tracks current state, manages base rental pricing calculations.
* **Attributes:** `asset_id` (str), `model_name` (str), `daily_rate` (float), `status` (str), `purchase_year` (int).
* **Methods:** `calculate_rental_cost(days: int) -> float`, `mark_maintenance()`, `mark_available()`, `to_dict() -> dict`, `from_dict(data: dict) -> Equipment`.
* **Relationships:** Parent class to specialized equipment models. Held in lists within `FleetService` and `Contract`.

### Class: `PoweredEquipment` (Subclass of `Equipment`)

* **Purpose:** Models machinery driven by internal engines or motors requiring fuel and hour tracking.
* **Responsibilities:** Manages run-hour accumulators, fuel capacities, and engine maintenance intervals.
* **Attributes:** Inherited attributes plus `current_hours` (float), `hours_at_last_service` (float), `service_interval_hours` (float), `fuel_capacity_gal` (float), `current_fuel_gal` (float).
* **Methods:** `record_usage(hours_added: float, fuel_remaining: float)`, `requires_service() -> bool` (Overrides parent/interface behavior), `to_dict()`, `from_dict()`.
* **Relationships:** Inherits from `Equipment`.

### Class: `Customer`

* **Purpose:** Represents a client business entity eligible to rent machinery.
* **Responsibilities:** Stores account standing, validates contact information, tracks balance states.
* **Attributes:** `customer_id` (str), `company_name` (str), `email` (str), `phone` (str), `has_unpaid_balance` (bool).
* **Methods:** `flag_delinquent()`, `clear_delinquent()`, `to_dict()`, `from_dict()`.
* **Relationships:** Referenced by `Contract` via `customer_id`.

### Class: `Contract`

* **Purpose:** Encapsulates an active or historical rental transaction.
* **Responsibilities:** Binds customer and equipment, calculates totals, tracks actual return dates and final surcharges.
* **Attributes:** `contract_id` (str), `customer_id` (str), `asset_id` (str), `start_date` (datetime), `planned_end_date` (datetime), `actual_return_date` (datetime | None), `initial_hours` (float), `return_hours` (float), `base_cost` (float), `penalty_fees` (float), `status` (str - `ACTIVE`, `CLOSED`, `CANCELLED`).
* **Methods:** `close_contract(return_date, final_hours, fuel_returned, fuel_fee_per_gal)`, `calculate_overdue_days() -> int`, `to_dict()`, `from_dict()`.
* **Relationships:** Links a single `Customer` and a single `Equipment` item.

### Class: `JSONRepository`

* **Purpose:** Manages safe file serialization and deserialization.
* **Responsibilities:** Reads raw JSON structures into memory, transforms them into domain objects via model factory methods, and commits updated domain object states safely back to disk files.
* **Attributes:** `file_path` (Path).
* **Methods:** `load_all() -> list[dict]`, `save_all(data: list[dict]) -> None`, `append_record(record: dict) -> None`.
* **Relationships:** Utilized by Service layer classes to store domain states.

### Class: `FleetService`

* **Purpose:** Orchestrates business operations for fleet assets and maintenance routines.
* **Responsibilities:** Registers assets, filters inventory, triggers maintenance flags, validates state transitions.
* **Attributes:** `repository` (JSONRepository), `equipment_list` (list[Equipment]).
* **Methods:** `add_equipment(equipment: Equipment)`, `get_available_assets() -> list[Equipment]`, `flag_for_service(asset_id: str)`, `update_hours_and_check_service(asset_id: str, new_hours: float)`.
* **Relationships:** Uses `JSONRepository` and manipulates `Equipment` instances.

### Class: `RentalService`

* **Purpose:** Orchestrates the rental workflow, validation rules, and financial calculations.
* **Responsibilities:** Verifies customer eligibility, issues contracts, updates asset statuses, calculates closure fees, updates persistence.
* **Attributes:** `fleet_service` (FleetService), `customer_repo` (JSONRepository), `contract_repo` (JSONRepository).
* **Methods:** `create_contract(customer_id: str, asset_id: str, duration_days: int) -> Contract`, `process_return(contract_id: str, return_hours: float, fuel_returned: float) -> Contract`.
* **Relationships:** Collaborates with `FleetService`, `Customer`, and `Contract`.

---

# 8. Data Flow

```text
                 [ User CLI Input ]
                         │
                         ▼
             [ Input Validator Module ]
            (Checks syntax, types, dates)
                         │
                         ▼
             [ Service Layer (Logic) ]
    (Enforces Business Rules & State Checks)
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
   [ Domain Model State ]     [ Custom Exception ]
  (Mutates Class Instances)   (If Rule Violated -> Alert CLI)
            │
            ▼
    [ Repository Layer ]
  (Serializes Class Objects)
            │
            ▼
   [ JSON Storage Files ]
  (Persistent Disk Storage)

```

---

# 9. Storage Requirements

The application must exclusively use **JSON files** within the `storage/` directory to persist state between executions.

* `fleet.json`: Stores all equipment assets (including specialized attributes like hour meters and fuel levels).
* `customers.json`: Stores client profiles and balance flags.
* `contracts.json`: Stores historical and active rental agreements.
* `maintenance.json`: Stores service logs and maintenance records.

*No database engines, ORMs, or third-party storage libraries may be used.*

---

# 10. User Inputs & Menu Interface

The CLI menu structure must present clear navigation prompts:

```text
==================================================
        APEX FIELD SYSTEMS - ASSET OPERATOR       
==================================================
1. Fleet Management
2. Customer Accounts
3. Rental Desk (Dispatch & Return)
4. Service & Maintenance Operations
5. Reports & Analytics
6. System Exit
==================================================
Select Option [1-6]:

```

### Menu Sub-Options & Expected Inputs

#### Option 1: Fleet Management

* **Add Equipment:** Prompt for Asset Tag ID, Category (`Powered` / `Static`), Model Name, Daily Rate, Purchase Year, (if Powered: Initial Hours, Service Interval, Fuel Capacity).
* **View Fleet Catalog:** Optional filter input (`All`, `Available`, `In Maintenance`, `Rented`).
* **Search Asset:** Prompt for Asset Tag ID or keyword string.

#### Option 2: Customer Accounts

* **Register Customer:** Prompt for Company Name, Corporate Email, Phone Number.
* **Search Customer:** Prompt for Customer ID or Company Name string.

#### Option 3: Rental Desk

* **Create Contract (Dispatch):** Prompt for Customer ID, Asset Tag ID, Rental Duration (Days).
* **Process Return:** Prompt for Contract ID, Actual Return Date, Current Hour Meter Reading, Fuel Level Returned (Gallons/Liters).
* **View Active Rentals:** List active contracts with pending return dates.

#### Option 4: Service & Maintenance Operations

* **Log Service Event:** Prompt for Asset Tag ID, Service Description, Repair Cost, Hours Reset Confirmation.
* **View Pending Service Queue:** Display assets flagged as `IN_MAINTENANCE`.

#### Option 5: Reports & Analytics

* **Generate Financial Summary:** Prompt for Start Date (`YYYY-MM-DD`) and End Date (`YYYY-MM-DD`).
* **Fleet Utilization Overview:** Display aggregate operational statistics immediately.

---

# 11. Validation Rules

The application must intercept bad inputs before they reach the service layer:

1. **Empty Strings:** Name, ID, category, and phone fields cannot consist of whitespace or empty entries.
2. **Positive Numeric Enforcement:** Rates, hour metrics, fuel quantities, and days must be strictly greater than zero.
3. **Date Syntax:** All date inputs must strictly adhere to `YYYY-MM-DD` format and parse into valid calendar dates.
4. **Hour Meter Monotonicity:** Returned hour readings must be greater than or equal to the hour reading logged at dispatch (hours cannot go backward).
5. **Fuel Level Boundaries:** Returned fuel gallons cannot exceed the maximum tank capacity of the asset.
6. **Email Format:** Customer emails must contain an `@` symbol and a valid domain extension dot (`.`).
7. **Phone Format:** Phone inputs must contain between 7 and 15 digits.
8. **Duplicate ID Interception:** Attempting to register an existing Asset ID or Customer ID must be rejected prior to record creation.

---

# 12. Exception Handling Requirements

Define a custom exception base class named `ApexPlatformError` derived from Python's built-in `Exception`. Implement specific sub-classes for handled operational errors:

```text
ApexPlatformError (Base)
├── AssetUnavailableError         # Triggered when attempting to rent an asset not in 'AVAILABLE' state
├── CustomerDelinquentError        # Triggered when customer has unpaid balance flag
├── RecordNotFoundError           # Triggered when an ID lookup fails across repos
├── InvalidStateTransitionError   # Triggered when illegal state changes are attempted
├── InvalidMeterReadingError      # Triggered when returned hours < initial hours
├── MaintenanceRequiredError      # Triggered when unserviced asset dispatch is attempted
└── StorageCorruptionError        # Triggered when JSON storage files are unparseable

```

The main menu loop must catch these custom exceptions, display clean error messaging to the operator, and keep the application execution running without crashing to the system terminal shell.

---

# 13. Recommended Python Libraries

Use **only** built-in Python modules. Do not install external packages.

* `json`: For disk persistence serialization/deserialization.
* `pathlib`: For robust cross-platform path handling.
* `datetime`: For contract date arithmetic and timestamp logging.
* `uuid`: For auto-generating short unique contract identifiers.
* `abc`: For defining abstract base classes (`ABC`, `@abstractmethod`).
* `typing`: For type hint definitions (`Optional`, `Union`, `List`, `Dict`).
* `dataclasses`: (Optional) For clean data-container definitions.

---

# 14. Stretch Goals

If you complete the core requirements ahead of schedule, consider adding these optional features:

* **CSV Operational Export:** Add an option in the Reports menu to dump financial summary tables to a `.csv` file in `data/exports/`.
* **Database Backup Utility:** Automatically create a timestamped backup copy of all `.json` files in `storage/backups/` upon system exit.
* **Audit Activity Logger:** Implement a file logger that appends every state change (e.g., `[2026-08-05 14:22:01] CONTRACT_CREATED: ID C-1029 BY USER Desk1`) to `storage/audit.log`.

---

# 15. Evaluation Checklist

Use this checklist to verify your solution prior to submitting it for client review:

* [ ] **OOP Structure:** Implements base `Equipment` class and specialized subclasses (`PoweredEquipment`) using inheritance.
* [ ] **Encapsulation:** Class attributes use properties/getters/setters to protect state variables (e.g., meter hours, fuel levels).
* [ ] **Polymorphism:** Method overriding used cleanly across model subclasses for custom calculations or maintenance checks.
* [ ] **File Persistence:** All asset, customer, contract, and maintenance changes persist accurately to JSON files and reload seamlessly upon application restart.
* [ ] **Error Safety:** Custom exception hierarchy created and caught smoothly in the CLI loop without unhandled stack traces.
* [ ] **Business Logic Integrity:** Overdue penalties, fuel surcharges, and auto-maintenance transitions trigger correctly according to specifications.
* [ ] **Input Safety:** Bad user inputs (e.g., text entered into rate fields, invalid dates, negative hours) are caught gracefully with user-friendly warnings.
* [ ] **Separation of Concerns:** Clear directory structure isolating Models, Services, Repositories, Utilities, and CLI interfaces.
* [ ] **Code Cleanliness:** Professional naming conventions, type hints applied throughout, clean module imports, and zero external dependencies.