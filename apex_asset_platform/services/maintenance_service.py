from datetime import datetime
from random import random
from models.maintenance_model.maintenance_log import MaintenanceLog
from repositories.json_repository import JSONRepository

def maintenance_id_generator() -> str:
    number = random.randint(1000, 10000)
    return str(f"MNT-{number}")
class MaintenanceService:
    """Business logic orchestration service for managing maintenance log history and JSON storage persistence.

    Attributes:
        maintenance_repository (JSONRepository): Repository instance managing storage/maintenance.json.
        maintenance_list (list[MaintenanceLog]): In-memory list cache of MaintenanceLog domain objects.
    """

    def __init__(self, maintenance_repository: JSONRepository) -> None:
        """Initializes MaintenanceService with repository dependency injection and populates memory cache.

        Args:
            maintenance_repository (JSONRepository): Data access repository for maintenance records.
        """
        self.maintenance_repository = maintenance_repository
        self.maintenance_list: list[MaintenanceLog] = []
        self._load_maintenance_cache()

    def _load_maintenance_cache(self) -> None:
        """Private helper method that loads raw JSON records from storage and hydrates maintenance_list."""
        for record in self.maintenance_repository.load_all():
            maintenance_obj = MaintenanceLog.from_dict(record)
            self.maintenance_list.append(maintenance_obj)

    def save_maintenance_cache(self) -> None:
        """Serializes in-memory MaintenanceLog domain objects back to storage/maintenance.json."""
        serialized_data = [item.to_dict() for item in self.maintenance_list]
        self.maintenance_repository.save_all(serialized_data)

    def append_maintenance_log(self, maintenance_log: MaintenanceLog) -> None:
        """Appends a new MaintenanceLog object to the in-memory cache and persists changes to JSON disk storage.

        Args:
            maintenance_log (MaintenanceLog): MaintenanceLog domain object to append and save.
        """
        maintenance_log.maintenance_id = maintenance_id_generator()
        maintenance_log.service_date = datetime.now().strftime("%Y-%m-%d")
        self.maintenance_list.append(maintenance_log)

