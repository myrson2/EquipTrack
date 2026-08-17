from .fleet_service import FleetService
from .rental_service import RentalService
from .maintenance_service import MaintenanceService

class ReportService:
    def __init__(self, fleet_service: FleetService, rental_service: RentalService, maintenance_service: MaintenanceService) -> None:
        self.fleet_service = fleet_service
        self.rental_service = rental_service
        self.maintenance_service = maintenance_service
    
    def get_fleet_utilization(self) -> dict[str, float]:
        fleet = self.fleet_service.equipment_list

        total = len(fleet)
        available = len([fleet for f in fleet if f.status.value == "AVAILABLE"])
        rented = len([fleet for f in fleet if f.status.value == "RENTED"])
        in_maintenance = len([fleet for f in fleet if f.status.value == "IN_MAINTENANCE"])

        return {
            "total_machinery_assets" : total,
            "available_equipment": available,
            "available_pct" : available / total,
            "rented_equipment": rented,
            "rented_pct" : rented / total,
            "in_maintenance_equipment": in_maintenance,
            "in_maintenance_pct" : in_maintenance / total
        }

        