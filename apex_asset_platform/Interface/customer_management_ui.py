from models.customer_model.customer import Customer
from services.customer_service import CustomerService

def display_customer_menu() -> None:
    """Displays the Customer Accounts sub-menu options."""
    print("==================================================")
    print("            CUSTOMER ACCOUNTS MENU               ")
    print("==================================================")
    print("1. Create Account")
    print("2. Registered Accounts")
    print("3. Accounts Status")
    print("4. Back to main menu")
    print("==================================================")

def handle_customer_management(customer_svc: CustomerService | None = None) -> None:
    """Handles interactive operator CLI workflow for Customer Accounts.

    Args:
        customer_svc (CustomerService, optional): Service layer handling customer accounts persistence.
    """
    while True:
        display_customer_menu()
        try:
            choice = input("Select Customer Option [1-4]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nReturning to Main Operator Menu...\n")
            break

        match choice:
            case "1":
                print("\n--- Create New Customer Account ---")
                try:
                    company_name = input("Enter Company Name: ").strip()
                    email = input("Enter Email Address: ").strip()
                    phone = input("Enter Phone Number: ").strip()

                    new_customer = Customer(
                        company_name=company_name,
                        email=email,
                        phone=phone,
                    )

                    if customer_svc:
                        customer_svc.register_customer(new_customer)

                    print(
                        f"\nSUCCESS: Created Account [{new_customer.customer_id}] {new_customer.company_name}!\n"
                    )
                except ValueError as err:
                    print(f"\nERROR: Invalid input details - {err}\n")

            case "2":
                print("\n--- Registered Accounts ---")
                if customer_svc:
                    accounts = customer_svc.get_all_customers()
                    if not accounts:
                        print("No customer accounts registered yet.\n")
                    else:
                        for acc in accounts:
                            print(str(acc))
                        print()
                else:
                    print("[Demo Mode] Displaying all registered accounts...\n")

            case "3":
                print("\n--- Accounts Status ---")
                status_choice = (
                    input("Select Account Status [a. PAID / b. UNPAID]: ").strip().lower()
                )

                if status_choice in ["a", "paid"]:
                    print("\n--- PAID Accounts (Good Standing) ---")
                    if customer_svc:
                        paid_acc = customer_svc.get_paid_customers()
                        if not paid_acc:
                            print("No paid accounts found in good standing.\n")
                        else:
                            for acc in paid_acc:
                                print(str(acc))
                            print()
                    else:
                        print("[Demo Mode] Showing PAID accounts...\n")

                elif status_choice in ["b", "unpaid"]:
                    print("\n--- UNPAID Accounts (Delinquent Status) ---")
                    if customer_svc:
                        unpaid_acc = customer_svc.get_unpaid_customers()
                        if not unpaid_acc:
                            print("No delinquent/unpaid accounts found.\n")
                        else:
                            for acc in unpaid_acc:
                                print(str(acc))
                            print()
                    else:
                        print("[Demo Mode] Showing UNPAID accounts...\n")
                else:
                    print("\nInvalid status choice. Select 'a' for PAID or 'b' for UNPAID.\n")

            case "4":
                print("\nReturning to Main Operator Menu...\n")
                break

            case _:
                print("\nInvalid choice. Please select a valid option [1-4].\n")
