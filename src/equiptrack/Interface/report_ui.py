from services.report_service import ReportService


def display_reports_menu() -> None:
    """Displays the Reports & Analytics sub-menu options."""
    print("==================================================")
    print("           REPORTS & ANALYTICS DASHBOARD          ")
    print("==================================================")
    print("1. Fleet Utilization Report (% RENTED vs AVAILABLE vs IN_MAINTENANCE)")
    print("2. Revenue & Yield Summary (Total Earnings from Contracts)")
    print("3. Total Maintenance Cost Analysis (Sum of Repair Costs)")
    print("4. Executive Overview (All Analytics Combined)")
    print("5. Back to Main Menu")
    print("==================================================")


def handle_report_operations(report_svc: ReportService | None = None) -> None:
    """Handles interactive operator CLI workflow for Reports & Analytics operations.

    Args:
        report_svc (ReportService, optional): Service layer managing analytics calculations and report data.
    """
    while True:
        display_reports_menu()
        try:
            choice = input("Select Analytics Option [1-5]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nReturning to Main Operator Menu...\n")
            break

        match choice:
            case "1":
                print("\n--- Fleet Utilization Report ---")
                if report_svc:
                    try:
                        utilization_data = report_svc.get_fleet_utilization()
                        print("\n==================================================")
                        print("             FLEET UTILIZATION REPORT             ")
                        print("==================================================")
                        print(f"Total Machinery Assets: {utilization_data.get('total_machinery_assets', 0)}")
                        print(f"Available Equipment:    {utilization_data.get('available_equipment', 0)} ({utilization_data.get('available_pct', 0.0):.1f}%)")
                        print(f"Rented Equipment:       {utilization_data.get('rented_equipment', 0)} ({utilization_data.get('rented_pct', 0.0):.1f}%)")
                        print(f"In Maintenance:         {utilization_data.get('in_maintenance_equipment', 0)} ({utilization_data.get('in_maintenance_pct', 0.0):.1f}%)")
                        print("==================================================\n")
                    except Exception as err:
                        print(f"\nERROR: Could not generate fleet utilization report: {err}\n")
                else:
                    print("Report Service not initialized.\n")

            case "2":
                print("\n--- Revenue & Yield Summary ---")
                if report_svc:
                    try:
                        revenue_data = report_svc.get_revenue_summary()
                        print("\n==================================================")
                        print("             REVENUE & YIELD SUMMARY              ")
                        print("==================================================")
                        print(f"Total Contracts Executed: {revenue_data.get('total_contracts', 0)}")
                        print(f"Base Rental Revenue:      ${revenue_data.get('base_revenue', 0.0):.2f}")
                        print(f"Late Fee Penalties:       ${revenue_data.get('late_penalties', 0.0):.2f}")
                        print(f"Fuel Surcharges:          ${revenue_data.get('fuel_surcharges', 0.0):.2f}")
                        print("--------------------------------------------------")
                        print(f"TOTAL GROSS REVENUE:      ${revenue_data.get('total_revenue', 0.0):.2f}")
                        print("==================================================\n")
                    except Exception as err:
                        print(f"\nERROR: Could not generate revenue summary report: {err}\n")
                else:
                    print("Report Service not initialized.\n")

            case "3":
                print("\n--- Total Maintenance Cost Analysis ---")
                if report_svc:
                    try:
                        maint_data = report_svc.get_maintenance_cost_analysis()
                        print("\n==================================================")
                        print("        MAINTENANCE COST ANALYSIS REPORT          ")
                        print("==================================================")
                        print(f"Total Service Events:   {maint_data.get('total_service_events', 0)}")
                        print(f"Average Repair Cost:    ${maint_data.get('average_service_cost', 0.0):.2f}")
                        print(f"TOTAL MAINTENANCE COST: ${maint_data.get('total_maintenance_cost', 0.0):.2f}")
                        print("==================================================\n")
                    except Exception as err:
                        print(f"\nERROR: Could not generate maintenance cost analysis: {err}\n")
                else:
                    print("Report Service not initialized.\n")

            case "4":
                print("\n--- Executive Overview (All Analytics Combined) ---")
                if report_svc:
                    try:
                        overview = report_svc.get_executive_overview()
                        print("\n==================================================")
                        print("           EXECUTIVE OPERATIONAL OVERVIEW         ")
                        print("==================================================")
                        print(f"Total Fleet Assets:     {overview.get('total_assets', 0)}")
                        print(f"Active Fleet Utilization: {overview.get('utilization_pct', 0.0):.1f}%")
                        print(f"Total Gross Revenue:     ${overview.get('total_revenue', 0.0):.2f}")
                        print(f"Total Maintenance Expenses: ${overview.get('total_maintenance_cost', 0.0):.2f}")
                        print(f"Net Operating Margin:   ${overview.get('net_operating_margin', 0.0):.2f}")
                        print("==================================================\n")
                    except Exception as err:
                        print(f"\nERROR: Could not generate executive overview: {err}\n")
                else:
                    print("Report Service not initialized.\n")

            case "5":
                print("\nReturning to Main Operator Menu...\n")
                break

            case _:
                print("\nERROR: Invalid choice. Please select an option between 1 and 5.\n")
