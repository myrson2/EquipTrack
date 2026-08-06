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

def main():
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
