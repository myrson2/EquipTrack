from pathlib import Path
import csv
import exceptions.custom_exceptions as custom_exceptions
import repositories.json_repository as json_repository
from Interface.fleet_management_ui import handle_fleet_management
from services.fleet_service import FleetService

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
        data_sample_path = Path("data_sample")
        if data_sample_path.is_dir():
            load_repository(data_sample_path)
    except Exception as e:
        print(f"Storage Initialization Notice: {e}")

    fleet_repo = json_repository.JSONRepository(Path("storage/fleet.json"))
    fleet_svc = FleetService(repository=fleet_repo)

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
                print("\nOpening Customer Accounts...\n")
            case "3":
                print("\nOpening Rental Desk...\n")
            case "4":
                print("\nOpening Service & Maintenance Operations...\n")
            case "5":
                print("\nOpening Reports & Analytics...\n")
            case "6":
                print("\nExiting system. Goodbye!")
                break
            case _:
                print("\nInvalid choice. Please select a valid option [1-6].\n")


if __name__ == "__main__":
    main()
