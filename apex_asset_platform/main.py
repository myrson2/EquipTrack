from pathlib import Path
import csv

from services import ReportService
from services.maintenance_service import MaintenanceService
import exceptions.custom_exceptions as custom_exceptions
import repositories.json_repository as json_repository
from interface.customer_management_ui import handle_customer_management
from interface.report_ui import handle_report_operations
from interface.fleet_management_ui import handle_fleet_management
from interface.rental_management_ui import handle_rental_service
from interface.maintenance_management_ui import handle_maintenance_operations
from services.customer_service import CustomerService
from services.fleet_service import FleetService
from services.rental_service import RentalService


def display_menu() -> None:
    """Displays the main terminal operator navigation menu."""
    print("==================================================")
    print("        APEX FIELD SYSTEMS - ASSET OPERATOR       ")
    print("==================================================")
    print("1. Fleet Management")
    print("2. Customer Accounts")
    print("3. Rental Desk (Dispatch & Return)")
    print("4. Service & Maintenance Operations")
    print("5. Reports & Analytics")
    print("6. System Exit")
    print("==================================================")

def load_repository(file_path: Path) -> None:
    """Initializes persistent storage directory from data_sample CSV files if missing.

    Args:
        file_path (Path): Path to data_sample directory containing initial CSV files.
    """
    for item in file_path.iterdir():
        if item.is_file() and item.suffix == ".csv":
            target_path = Path("storage") / f"{item.stem}.json"
            if not target_path.exists():
                json_repo = json_repository.JSONRepository(target_path)
                with item.open("r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    temp_storage = list(reader)
                json_repo.save_all(temp_storage)

def main() -> None:
    """Application entry point and main terminal loop."""
    try:
        data_sample_path = Path(__file__).parent / "data_sample"
        if data_sample_path.exists():
            load_repository(data_sample_path)
    except Exception as e:
        print(f"Storage Initialization Notice: {e}")

    fleet_repo = json_repository.JSONRepository(Path("storage/fleet.json"))
    mtn_repo = json_repository.JSONRepository(Path("storage/maintenance.json"))
    customer_repo = json_repository.JSONRepository(Path("storage/customers.json"))
    contract_repo = json_repository.JSONRepository(Path("storage/contracts.json"))

    mtn_svc = MaintenanceService(maintenance_repository=mtn_repo)
    fleet_svc = FleetService(fleet_repository=fleet_repo, maintenance_service=mtn_svc)
    customer_svc = CustomerService(customer_repository=customer_repo)
    rental_svc = RentalService(contract_repository=contract_repo, fleet_service=fleet_svc, customer_service=customer_svc)
    report_svc = ReportService(fleet_service=fleet_svc, rental_service=rental_svc, maintenance_service=mtn_svc)

    fleet_svc.save_fleet_cache()
    customer_svc.save_customer_cache()
    rental_svc.save_contract_cache()
    mtn_svc.save_maintenance_cache()

    while True:
        display_menu()
        try:
            option = input("Select Option [1-6]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting system. Goodbye!")
            break

        match option:
            case "1":
                handle_fleet_management(fleet_svc)
            case "2":
                handle_customer_management(customer_svc)
            case "3":
                handle_rental_service(rental_svc)
            case "4":
                handle_maintenance_operations(fleet_svc, mtn_svc)
            case "5":
                handle_report_operations(report_svc)
            case "6":
                print("\nExiting system. Goodbye!")
                # safely save all data to JSON files
                fleet_svc.save_fleet_cache()
                customer_svc.save_customer_cache()
                rental_svc.save_contract_cache()
                mtn_svc.save_maintenance_cache()
                break
            case _:
                print("\nInvalid choice. Please select a valid option [1-6].\n")


if __name__ == "__main__":
    main()
