from models.fleet_management_models.fleet_enum import EquipmentStatus
from services.customer_service import CustomerService
from services.fleet_service import FleetService
from services.maintenance_service import MaintenanceService
from services.rental_service import RentalService


class ReportService:
    """Business logic orchestration service for aggregating platform analytics and generating executive reports.

    Attributes:
        fleet_service (FleetService): Injected service managing fleet machinery inventory.
        rental_service (RentalService): Injected service managing customer rental contracts.
        maintenance_service (MaintenanceService): Injected service managing historical service logs.
        customer_service (CustomerService, optional): Injected service managing customer account standings.
    """

    def __init__(
        self,
        fleet_service: FleetService,
        rental_service: RentalService,
        maintenance_service: MaintenanceService,
        customer_service: CustomerService | None = None,
    ) -> None:
        """Initializes ReportService with injected service layer dependencies.

        Args:
            fleet_service (FleetService): Fleet management service instance.
            rental_service (RentalService): Rental operations service instance.
            maintenance_service (MaintenanceService): Maintenance service instance.
            customer_service (CustomerService, optional): Customer account service instance.
        """
        self.fleet_service = fleet_service
        self.rental_service = rental_service
        self.maintenance_service = maintenance_service
        self.customer_service = customer_service

    def get_fleet_utilization(self) -> dict:
        """Calculates fleet utilization metrics including total counts and percentage rates by operational status.

        Returns:
            dict: Dictionary matching interface/report_ui.py schema containing total_assets, available_count,
                  available_pct, rented_count, rented_pct, maintenance_count, and maintenance_pct.
        """
        fleet = self.fleet_service.equipment_list
        total = len(fleet)

        if total == 0:
            return {
                "total_assets": 0,
                "available_count": 0,
                "available_pct": 0.0,
                "rented_count": 0,
                "rented_pct": 0.0,
                "maintenance_count": 0,
                "maintenance_pct": 0.0,
            }

        available = len([f for f in fleet if f.status == EquipmentStatus.AVAILABLE or getattr(f.status, "value", f.status) == "AVAILABLE"])
        rented = len([f for f in fleet if f.status == EquipmentStatus.RENTED or getattr(f.status, "value", f.status) == "RENTED"])
        in_maintenance = len([f for f in fleet if f.status == EquipmentStatus.IN_MAINTENANCE or getattr(f.status, "value", f.status) == "IN_MAINTENANCE"])

        return {
            "total_assets": total,
            "available_count": available,
            "available_pct": (available / total) * 100.0,
            "rented_count": rented,
            "rented_pct": (rented / total) * 100.0,
            "maintenance_count": in_maintenance,
            "maintenance_pct": (in_maintenance / total) * 100.0,
        }

    def get_revenue_summary(self) -> dict:
        """Calculates total gross revenue generated from all rental contracts.

        Returns:
            dict: Dictionary matching interface/report_ui.py schema containing total_contracts, base_revenue,
                  late_penalties, fuel_surcharges, and total_revenue.
        """
        contracts = self.rental_service.contract_list
        total_contracts = len(contracts)

        base_rev = sum(float(getattr(c, "base_cost", 0.0) or 0.0) for c in contracts)
        penalties = sum(float(getattr(c, "penalty_fees", 0.0) or 0.0) for c in contracts)

        fuel_fees = 0.0
        for c in contracts:
            if hasattr(c, "fuel_at_dispatch_gal") and hasattr(c, "fuel_returned_gal"):
                dispatch_fuel = float(getattr(c, "fuel_at_dispatch_gal", 0.0) or 0.0)
                returned_fuel = float(getattr(c, "fuel_returned_gal", 0.0) or 0.0)
                if returned_fuel < dispatch_fuel:
                    deficit = dispatch_fuel - returned_fuel
                    fuel_fees += (deficit * 5.0) + 50.0

        total_gross = base_rev + penalties + fuel_fees

        return {
            "total_contracts": total_contracts,
            "base_revenue": base_rev,
            "late_penalties": penalties,
            "fuel_surcharges": fuel_fees,
            "total_revenue": total_gross,
        }

    def get_maintenance_cost_analysis(self) -> dict:
        """Calculates total maintenance repair expenditures from recorded service log receipts.

        Returns:
            dict: Dictionary matching interface/report_ui.py schema containing total_service_events,
                  total_maintenance_cost, and average_service_cost.
        """
        logs = self.maintenance_service.maintenance_list
        total_events = len(logs)

        total_cost = sum(float(getattr(log, "cost", 0.0) or 0.0) for log in logs)
        avg_cost = (total_cost / total_events) if total_events > 0 else 0.0

        return {
            "total_service_events": total_events,
            "total_maintenance_cost": total_cost,
            "average_service_cost": avg_cost,
        }

    def get_executive_overview(self) -> dict:
        """Combines fleet utilization, revenue earnings, and maintenance expenses into an executive overview.

        Returns:
            dict: Dictionary matching interface/report_ui.py schema containing total_assets, utilization_pct,
                  total_revenue, total_maintenance_cost, and net_operating_margin.
        """
        utilization = self.get_fleet_utilization()
        revenue = self.get_revenue_summary()
        maintenance = self.get_maintenance_cost_analysis()

        gross_rev = revenue["total_revenue"]
        maint_cost = maintenance["total_maintenance_cost"]
        net_margin = gross_rev - maint_cost

        return {
            "total_assets": utilization["total_assets"],
            "utilization_pct": utilization["rented_pct"],
            "total_revenue": gross_rev,
            "total_maintenance_cost": maint_cost,
            "net_operating_margin": net_margin,
        }