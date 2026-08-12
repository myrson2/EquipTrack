from services.rental_service import RentalService

def display_rental_menu() -> None:
    """Displays the Rental Desk (Dispatch & Return) sub-menu options."""
    print("==================================================")
    print("        RENTAL DESK (DISPATCH & RETURN)          ")
    print("==================================================")
    print("1. Dispatch / Issue Rental Contract")
    print("2. Process Equipment Return & Checkout")
    print("3. View Active Rental Agreements")
    print("4. Search Contract by ID")
    print("5. Back to Main Menu")
    print("==================================================")


def handle_rental_service(rental_svc: RentalService | None = None) -> None:
    """Handles interactive operator CLI workflow for Rental Desk operations.

    Args:
        rental_svc (RentalService, optional): Service layer managing rental contracts.
    """
    while True:
        display_rental_menu()
        try:
            choice = input("Select Rental Desk Option [1-5]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nReturning to Main Operator Menu...\n")
            break

        match choice:
            case "1":
                print("\n--- Dispatch / Issue Rental Contract ---")
                try:
                    customer_id = input("Enter Customer ID (e.g. CUST-5001): ").strip()
                    asset_id = input("Enter Equipment Asset ID (e.g. EQ-1001): ").strip()
                    duration_str = input("Enter Rental Duration (days): ").strip()

                    if not duration_str.isdigit() or int(duration_str) <= 0:
                        print("\nERROR: Duration days must be a positive integer.\n")
                        continue

                    duration_days = int(duration_str)

                    if rental_svc:
                        contract = rental_svc.create_contract(
                            customer_id=customer_id,
                            asset_id=asset_id,
                            duration_days=duration_days,
                        )
                        print("\n==================================================")
                        print("       SUCCESS: RENTAL CONTRACT DISPATCHED       ")
                        print("==================================================")
                        print(f"Contract ID:        {contract.contract_id}")
                        print(f"Customer ID:        {contract.customer_id}")
                        print(f"Asset ID:           {contract.asset_id}")
                        print(f"Start Date:         {contract.start_date}")
                        print(f"Planned End Date:   {contract.planned_end_date}")
                        print(f"Daily Rate:         ${contract.daily_rate:.2f}/day")
                        print(f"Base Cost Owed:     ${contract.base_cost:.2f}")
                        print(f"Contract Status:    {contract.status}")
                        print("==================================================\n")
                except ValueError as err:
                    print(f"\nERROR: Could not dispatch contract - {err}\n")

            case "2":
                print("\n--- Process Equipment Return & Checkout ---")
                try:
                    contract_id = input("Enter Contract ID (e.g. CNTR-5001): ").strip()
                    return_hours_str = input("Enter Engine Hour Odometer Reading at Return: ").strip()
                    fuel_returned_str = input("Enter Fuel Level at Return (gallons): ").strip()
                    paid_input = input("Is invoice paid at counter? (y/n, default 'y'): ").strip().lower()

                    is_paid = paid_input != "n"
                    return_hours = float(return_hours_str) if return_hours_str else 0.0
                    fuel_returned = float(fuel_returned_str) if fuel_returned_str else 0.0

                    if rental_svc:
                        contract = rental_svc.process_return(
                            contract_id=contract_id,
                            return_hours=return_hours,
                            fuel_returned_gal=fuel_returned,
                            is_paid=is_paid,
                        )
                        print("\n==================================================")
                        print("        SUCCESS: CONTRACT RETURN PROCESSED        ")
                        print("==================================================")
                        print(f"Contract ID:        {contract.contract_id}")
                        print(f"Actual Return Date: {contract.actual_return_date}")
                        print(f"Return Run Hours:   {contract.return_hours} hrs")
                        print(f"Fuel Returned:      {contract.fuel_returned_gal} gal")
                        print(f"Base Rental Cost:   ${contract.base_cost:.2f}")
                        print(f"Penalty Fees:       ${contract.penalty_fees:.2f}")
                        total_cost = contract.base_cost + contract.penalty_fees
                        print(f"Total Amount Owed:  ${total_cost:.2f}")
                        print(f"Contract Status:    {contract.status}")
                        print("==================================================\n")
                except ValueError as err:
                    print(f"\nERROR: Could not process return - {err}\n")

            case "3":
                print("\n--- Active Rental Agreements ---")
                if rental_svc:
                    active_contracts = rental_svc.get_active_contracts()
                    if not active_contracts:
                        print("\nNotice: No active rental contracts currently on rent.\n")
                    else:
                        print(f"\nFound {len(active_contracts)} Active Contract(s):")
                        print("-" * 65)
                        for c in active_contracts:
                            print(
                                f"[{c.contract_id}] Customer: {c.customer_id} | Asset: {c.asset_id} | "
                                f"Start: {c.start_date} -> Due: {c.planned_end_date} | Rate: ${c.daily_rate:.2f}/day"
                            )
                        print("-" * 65 + "\n")

            case "4":
                print("\n--- Search Contract by ID ---")
                try:
                    search_id = input("Enter Contract ID (e.g. CNTR-5001): ").strip()
                    if rental_svc:
                        contract = rental_svc.get_contract_by_id(search_id)
                        print("\n==================================================")
                        print(f"               CONTRACT RECEIPT: {contract.contract_id}")
                        print("==================================================")
                        print(f"Customer ID:           {contract.customer_id}")
                        print(f"Asset ID:              {contract.asset_id}")
                        print(f"Start Date:            {contract.start_date}")
                        print(f"Planned End Date:      {contract.planned_end_date}")
                        print(f"Actual Return Date:    {contract.actual_return_date or 'N/A (On Rent)'}")
                        print(f"Initial Run Hours:     {contract.initial_hours} hrs")
                        print(f"Return Run Hours:      {contract.return_hours if contract.return_hours is not None else 'N/A'}")
                        print(f"Fuel at Dispatch:      {contract.fuel_at_dispatch_gal} gal")
                        print(f"Fuel at Return:        {contract.fuel_returned_gal if contract.fuel_returned_gal is not None else 'N/A'}")
                        print(f"Daily Rate:            ${contract.daily_rate:.2f}/day")
                        print(f"Base Cost:             ${contract.base_cost:.2f}")
                        print(f"Penalty Fees:          ${contract.penalty_fees:.2f}")
                        print(f"Total Amount Owed:     ${contract.base_cost + contract.penalty_fees:.2f}")
                        print(f"Status:                {contract.status}")
                        print("==================================================\n")
                except ValueError as err:
                    print(f"\nERROR: {err}\n")

            case "5":
                print("\nReturning to Main Operator Menu...\n")
                break
            case _:
                print("\nInvalid choice. Please select a valid option [1-5].\n")