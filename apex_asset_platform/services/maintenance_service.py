from apex_asset_platform.models.maintenance_model.maintenance_log import MaintenanceLog
from repositories.json_repository import JSONRepository

class MaintenanceService: 
    def __init__(self, maintenance_repository: JSONRepository) -> None : 
        self.maintenance_repository = maintenance_repository
        self.maintenance_list = list[MaintenanceLog] = []
        self._load_maintenance_cache()
    
    def _load_maintenance_cache(self):
        for record in self.maintenance_repository.load_all():
            maintenance_obj = MaintenanceLog.from_dict(record)
            self.maintenance_list.append(maintenance_obj)

    def save_maintenance_cache(self):
        serialized_data = [item.to_dict() for item in self.maintenance_list]
        self.maintenance_repository.save_all(serialized_data)

