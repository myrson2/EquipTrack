from models.maintenance_model.maintenance_log import MaintenanceLog
from services.fleet_service import FleetService
from services.maintenance_service import MaintenanceService

import random
from datetime import datetime


def display_maintenance_menu() -> None:
    """Displays the Service & Maintenance Operations sub-menu options."""
    print("==================================================")
    print("        SERVICE & MAINTENANCE OPERATIONS          ")
    print("==================================================")
    print("1. View Equipment Pending Maintenance (IN_MAINTENANCE)")
    print("2. Complete Maintenance & Restore to Inventory (IN_MAINTENANCE -> AVAILABLE)")
    print("3. Manually Flag Equipment for Service (AVAILABLE -> IN_MAINTENANCE)")
    print("4. View Maintenance Logs & Service History")
    print("5. Back to Main Menu")
    print("==================================================")


def handle_maintenance_operations(
    fleet_svc: FleetService | None = None,
    mtn_svc: MaintenanceService | None = None,
) -> None:
    """Handles interactive operator CLI workflow for Service & Maintenance Operations.

    Args:
        fleet_svc (FleetService, optional): Service layer managing fleet inventory and machinery status.
        mtn_svc (MaintenanceService, optional): Service layer managing historical maintenance log receipts.
    """
    while True:
        display_maintenance_menu()
        try:
            choice = input("Select Maintenance Option [1-5]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nReturning to Main Operator Menu...\n")
            break

        match choice:
            case "1":
                print("\n--- Equipment Pending Maintenance (IN_MAINTENANCE) ---")
                if fleet_svc:
                    pending_items = fleet_svc.get_in_maintenance_equipment()
                    if not pending_items:
                        print("No equipment currently in maintenance status.\n")
                    else:
                        print(f"\nFound {len(pending_items)} equipment item(s) pending maintenance:")
                        for item in pending_items:
                            print(f"  • {item}")
                        print()

            case "2":
                print("\n--- Complete Maintenance & Restore to Inventory ---")
                try:
                    asset_id = input("Enter Asset ID (e.g. EQ-1001): ").strip()
                    tech_name = input("Enter Technician/Mechanic Name: ").strip()
                    description = input("Enter Service/Repair Description: ").strip()
                    cost_str = input("Enter Total Service Cost ($USD): ").strip()

                    try:
                        cost_val = float(cost_str)
                        if cost_val < 0:
                            print("\nERROR: Service cost cannot be negative.\n")
                            continue
                    except ValueError:
                        print("\nERROR: Invalid cost amount entered.\n")
                        continue

                    if fleet_svc:
                        # 1. Fetch equipment to verify existence and meter reading
                        equipment = fleet_svc.get_equipment_by_id(asset_id)
                        meter_reading = getattr(equipment, "current_hours", 0.0)

                        # # 2. Generate unique MaintenanceLog ID
                        # log_id = f"MNT-{random.randint(9000, 9999)}"
                        # today_str = datetime.now().strftime("%Y-%m-%d")

                        log_obj = MaintenanceLog(
                            asset_id=asset_id,
                            description=description,
                            cost=cost_val,
                            meter_hours_at_service=meter_reading,
                            performed_by=tech_name,
                        )

                        # 3. Complete maintenance workflow
                        fleet_svc.complete_maintenance(log_obj)

                        print("\n==================================================")
                        print("        MAINTENANCE COMPLETED SUCCESSFULLY        ")
                        print("==================================================")
                        print(f"Log ID:          {log_obj.maintenance_id}")
                        print(f"Asset ID:        {log_obj.asset_id}")
                        print(f"Status:          AVAILABLE (Restored to Inventory)")
                        print(f"Technician:      {log_obj.performed_by}")
                        print(f"Service Cost:    ${log_obj.cost:.2f}")
                        print("==================================================\n")
                except ValueError as err:
                    print(f"\nERROR: {err}\n")
                except Exception as err:
                    print(f"\nUNEXPECTED ERROR: {err}\n")

            case "3":
                print("\n--- Manually Flag Equipment for Service ---")
                try:
                    asset_id = input("Enter Asset ID to flag (e.g. EQ-1001): ").strip()
                    if fleet_svc:
                        fleet_svc.flag_for_service(asset_id)
                        print(f"\nSUCCESS: Equipment '{asset_id}' flagged for IN_MAINTENANCE.\n")
                except ValueError as err:
                    print(f"\nERROR: {err}\n")
                except Exception as err:
                    print(f"\nUNEXPECTED ERROR: {err}\n")

            case "4":
                print("\n--- Maintenance Logs & Service History ---")
                if mtn_svc:
                    logs = mtn_svc.maintenance_list
                    if not logs:
                        print("No maintenance logs found in service history.\n")
                    else:
                        print(f"\nFound {len(logs)} historical maintenance log(s):")
                        for log in sorted(logs):
                            print(f"  • {log}")
                        print()

            case "5":
                print("\nReturning to Main Operator Menu...\n")
                break

            case _:
                print("\nERROR: Invalid selection. Please choose an option between 1 and 5.\n")
