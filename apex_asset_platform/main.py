from pathlib import Path
import csv
import exceptions.custom_exceptions as custom_exceptions
import repositories.json_repository as json_repository

def display_menu():
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

def load_repository(file_path) -> None:
    for item in file_path.iterdir():
        temp_storage = []
        if item.is_file() and item.suffix == ".csv":
            # Extracting the file name as name of the instance then direct it to the storage/f"{name}.json"
            target_path = Path("storage") / f"{item.stem}.json"
            json_repo = json_repository.JSONRepository(target_path)

            with item.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f) # Already written in dictionary
                temp_storage = list(reader) # Convert in list

            json_repo.save_all(temp_storage)
        else:
            print(f"File '{item.name}' is not a csv!")
            continue
    return None

def main():
    try:
        path = Path("data_sample")
        if path.is_dir():
            print(f"'{path}' is a directory!")
            load_repository(path)
        elif not path.exists():
            raise custom_exceptions.DirectoryNotFoundException(f"'{path}' does not exist!")
    except (custom_exceptions.DirectoryNotFoundException, custom_exceptions.FileNotFoundException) as e:
        print(e)

    while True:
        display_menu()
        try:
            option = input("Select Option [1-6]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting system. Goodbye!")
            break

        match option:
            case "1":
                print("\nOpening Fleet Management...\n")
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
