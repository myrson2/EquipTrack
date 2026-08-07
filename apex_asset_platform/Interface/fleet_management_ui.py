from models.fleet_management_models.base_equipment import BaseEquipment
from models.fleet_management_models.enum import EquipmentStatus
from models.fleet_management_models.powered_equipment import PoweredEquipment
from services.fleet_service import FleetService

def display_fleet_menu() -> None:
    """Displays the Fleet Management sub-menu options."""
    print("==================================================")
    print("              FLEET MANAGEMENT MENU              ")
    print("==================================================")
    print("1. Add New Equipment")
    print("2. View Fleet Catalog")
    print("3. Search Asset by Tag ID")
    print("4. Update Equipment Parameters & Status")
    print("5. Back to Main Menu")
    print("==================================================")


def handle_fleet_management(fleet_svc: FleetService) -> None:
    """Handles interactive operator CLI workflows for Fleet Management.

    Args:
        fleet_svc (FleetService): Initialized FleetService instance.
    """
    while True:
        display_fleet_menu()
        try:
            choice = input("Select Fleet Option [1-4]: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        match choice:
            case "1":
                print("\n--- Register New Equipment ---")
                try:
                    asset_id = input("Enter Asset Tag ID (e.g. EQ-1011): ").strip()
                    cat_input = input("Enter Category (STATIC / POWERED): ").strip().upper()
                    model_name = input("Enter Model Name: ").strip()
                    daily_rate = float(input("Enter Daily Rate ($): ").strip())
                    purchase_year = int(input("Enter Purchase Year (YYYY): ").strip())

                    if cat_input == "POWERED":
                        current_hours = float(input("Enter Initial Hours Meter: ").strip())
                        service_interval = float(input("Enter Service Interval Hours (e.g. 100): ").strip())
                        fuel_capacity = float(input("Enter Fuel Tank Capacity (Gallons): ").strip())

                        equipment = PoweredEquipment(
                            asset_id=asset_id,
                            model_name=model_name,
                            daily_rate=daily_rate,
                            purchase_year=purchase_year,
                            status=EquipmentStatus.AVAILABLE,
                            current_hours=current_hours,
                            hours_at_last_service=current_hours,
                            service_interval_hours=service_interval,
                            fuel_capacity_gallons=fuel_capacity,
                            current_fuel_gal=fuel_capacity,
                        )
                    else:
                        equipment = BaseEquipment(
                            asset_id=asset_id,
                            model_name=model_name,
                            daily_rate=daily_rate,
                            purchase_year=purchase_year,
                            status=EquipmentStatus.AVAILABLE,
                        )

                    fleet_svc.add_equipment(equipment)
                    print(
                        f"\nSUCCESS: Registered {equipment.model_name} [{equipment.asset_id}] into fleet catalog!\n")
                except ValueError as err:
                    print(f"\nERROR: Invalid input or duplicate asset ID - {err}\n")

            case "2":
                print("\n--- Fleet Catalog ---")
                print("1. All Fleet Assets")
                print("2. Available Assets Only")
                print("3. Assets in Maintenance")
                print("4. Rented Assets")
                print("5. Back to Main Menu")

                filter_choice = input("Select Filter Option [1-5]: ").strip()
                assets = []

                match filter_choice:
                    case "1":
                        assets = fleet_svc.get_all_equipment()
                        print("\n--- Full Fleet Catalog ---")
                    case "2":
                        assets = fleet_svc.get_available_assets()
                        print("\n--- Available Machinery ---")
                    case "3":
                        assets = fleet_svc.get_in_maintenance_equipment()
                        print("\n--- Assets in Maintenance ---")
                        pass
                    case "4":
                        assets = fleet_svc.get_rented_equipment()
                        print("\n--- Rented Assets ---")
                        pass
                    case "5":
                        continue
                    case _:
                        print("\nInvalid selection. Showing full catalog by default.")
                        assets = fleet_svc.get_all_equipment()

                if not assets:
                    print("No equipment records found.\n")
                else:
                    for asset in assets:
                        print(str(asset))
                    print()

            case "3":
                print("\n--- Search Asset ---")
                search_id = input("Enter Asset Tag ID to Search: ").strip()
                try:
                    asset = fleet_svc.get_equipment_by_id(search_id)
                    print(f"\nFOUND RECORD: {repr(asset)}")
                    print(f"Details: {str(asset)}\n")
                except ValueError as err:
                    print(f"\nERROR: {err}\n")

            case "4":

                pass

            case "5":
                print("\nReturning to Main Operator Menu...\n")
                break

            case _:
                print("\nInvalid choice. Select [1-4].\n")
