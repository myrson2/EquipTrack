import random
from models.fleet_management_models.base_equipment import BaseEquipment, EquipmentType, EquipmentStatus
from models.fleet_management_models.powered_equipment import PoweredEquipment
from repositories.json_repository import JSONRepository
from utils.validators import validate_unique_ids

def asset_id_generator() -> str:
    number = random.randint(1000, 10000)
    return str(f"EQ-{number}")

class FleetService:
    """Business logic orchestration service for managing fleet inventory, maintenance flags, and usage updates.

    Attributes:
        repository (JSONRepository): Data access repository for persistent JSON storage operations.
        equipment_list (list[BaseEquipment]): In-memory cache of fleet machinery instances.
    """

    def __init__(self, repository: JSONRepository) -> None:
        """Initializes FleetService with repository dependency injection and loads in-memory catalog.

        Args:
            repository (JSONRepository): Persistent JSON storage repository instance.
        """
        self.repository = repository
        self.equipment_list: list[BaseEquipment] = []
        self._load_initial_fleet()

    def _load_initial_fleet(self) -> None:
        """Private helper method that loads raw JSON records from storage and populates equipment_list with objects."""
        raw_records = self.repository.load_all()
        for record in raw_records:
            eq_type = record.get("equipment_type")
            if eq_type == EquipmentType.POWERED.value or eq_type == "POWERED":
                obj = PoweredEquipment(
                    asset_id=record.get("asset_id"),
                    model_name=record["model_name"],
                    daily_rate=float(record["daily_rate"]),
                    purchase_year=int(record["purchase_year"]),
                    status=EquipmentStatus(record["status"]),
                    current_hours=float(record.get("current_hours", 0.0)),
                    hours_at_last_service=float(record.get("hours_at_last_service", 0.0)),
                    service_interval_hours=float(record.get("service_interval_hours", 100.0)),
                    fuel_capacity_gallons=float(record.get("fuel_capacity_gal", record.get("fuel_capacity_gallons", 0.0))),
                    current_fuel_gal=float(record.get("current_fuel_gal", 0.0)),
                )
            else:
                obj = BaseEquipment(
                    asset_id=record.get("asset_id"),
                    model_name=record["model_name"],
                    daily_rate=float(record["daily_rate"]),
                    purchase_year=int(record["purchase_year"]),
                    status=EquipmentStatus(record["status"]),
                )
            self.equipment_list.append(obj)

    def save_equipment_list_to_storage(self) -> None:
        """Persists all in-memory equipment objects back to JSON disk storage."""
        serialized_data = [item.to_dict() for item in self.equipment_list]
        self.repository.save_all(serialized_data)

    def add_equipment(self, equipment: BaseEquipment) -> None:
        """Registers a new equipment asset into the fleet catalog.

        Args:
            equipment (BaseEquipment): New equipment or powered equipment instance to add.

        Raises:
            ValueError: If an asset with the same asset_id already exists.
        """

        generated_id = asset_id_generator()

        if validate_unique_ids(generated_id, self.equipment_list):
            equipment.asset_id = generated_id
            self.equipment_list.append(equipment)
            self.save_equipment_list_to_storage()
        else:
            raise ValueError(f"Equipment with ID '{equipment.asset_id}' already exists.")


    def get_all_equipment(self) -> list[BaseEquipment]:
        """Retrieves all equipment items in the catalog sorted by asset_id.

        Returns:
            list[BaseEquipment]: Sorted list of all fleet machinery objects.
        """
        return sorted(self.equipment_list)

    def get_available_assets(self) -> list[BaseEquipment]:
        """Filters catalog for machinery currently available for rental.

        Returns:
            list[BaseEquipment]: List of equipment instances where status is AVAILABLE.
        """
        return [item for item in self.equipment_list if item.status == EquipmentStatus.AVAILABLE]

    def get_in_maintenance_equipment(self) -> list[BaseEquipment]:
        return [item for item in self.equipment_list if item.status == EquipmentStatus.IN_MAINTENANCE]

    def get_rented_equipment(self) -> list[BaseEquipment]:
        return[item for item in self.equipment_list if item.status == EquipmentStatus.RENTED]

    def get_equipment_by_id(self, asset_id: str) -> BaseEquipment:
        """Searches for a specific equipment item by its unique asset_id.

        Args:
            asset_id (str): Unique asset tag identifier.

        Returns:
            BaseEquipment: Matching equipment instance.

        Raises:
            ValueError: If no equipment with asset_id is found.
        """
        for item in self.equipment_list:
            if item.asset_id == asset_id:
                return item
        raise ValueError(f"Equipment with ID '{asset_id}' not found.")

    def flag_for_service(self, asset_id: str) -> None:
        """Manually flags a specific equipment asset for maintenance.

        Args:
            asset_id (str): Unique asset tag identifier.

        Raises:
            ValueError: If equipment with asset_id is not found.
        """
        item = self.get_equipment_by_id(asset_id)
        item.mark_maintenance()
        self.save_equipment_list_to_storage()

    def update_hours_and_check_service(self, asset_id: str, hours_added: float, fuel_remaining: float) -> bool:
        """Updates operating hours and fuel level for powered machinery, auto-flagging maintenance if threshold is reached.

        Args:
            asset_id (str): Unique asset tag identifier.
            hours_added (float): Non-negative run-hours added during rental.
            fuel_remaining (float): Remaining fuel level in gallons.

        Returns:
            bool: True if equipment reached service threshold and was flagged IN_MAINTENANCE, False otherwise.

        Raises:
            ValueError: If asset_id is not found or is not a PoweredEquipment instance.
        """
        item = self.get_equipment_by_id(asset_id)
        if not isinstance(item, PoweredEquipment):
            raise ValueError(f"Asset ID '{asset_id}' is not a PoweredEquipment!")

        item.record_usage(hours_added, fuel_remaining)

        service_needed = False
        if item.requires_service():
            item.mark_maintenance()
            service_needed = True

        self.save_equipment_list_to_storage()
        return service_needed

    def update_equipment_status(self, fleet_item: BaseEquipment) -> None:
        """Completes maintenance for an asset, restoring status to AVAILABLE.

        Args:
            fleet_item (BaseEquipment): Equipment instance to update.
        """
        fleet_item.mark_available()

        if isinstance(fleet_item, PoweredEquipment):
            fleet_item.hours_at_last_service = fleet_item.current_hours

        self.save_equipment_list_to_storage()
