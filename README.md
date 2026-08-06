# Apex Field Systems - Asset Operator (EquipTrack)

Apex Field Systems - Asset Operator is a terminal-based fleet management and rental tracking platform designed to orchestrate equipment lifecycles, customer profiles, rental agreements, maintenance events, and analytics.

---

## 📂 Project Structure

```
apex_asset_platform/
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

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ (required for `match/case` statement support)

### Run the Application
From the workspace root directory, start the CLI application loop:
```bash
python apex_asset_platform/main.py
```

---

## 🛠️ Features (CLI Menu)

1. **Fleet Management**: Catalog specialized equipment, monitor availability states, and manage inventory.
2. **Customer Accounts**: Maintain customer profiles and rental eligibility details.
3. **Rental Desk (Dispatch & Return)**: Manage the lifecycle of rental agreements, dispatch assets, process returns, and calculate billing.
4. **Service & Maintenance Operations**: Log service events and manage scheduled maintenance cycles.
5. **Reports & Analytics**: Generate performance summaries, revenue statements, and utilization metrics.
