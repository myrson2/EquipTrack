class MaintenanceLog:
    """Domain model representing a recorded maintenance service event for a fleet asset.

    Attributes:
        maintenance_id (str): Unique maintenance log tag (e.g., 'MNT-9001').
        asset_id (str): Unique asset tag ID of equipment serviced.
        service_date (str): Date string of service completion (YYYY-MM-DD).
        description (str): Detailed description of repair/service performed.
        cost (float): Total service cost in USD.
        meter_hours_at_service (float): Hour meter reading when service was performed.
        performed_by (str): Name or ID of technician/mechanic who completed service.
    """

    def __init__(
        self,
        maintenance_id: str,
        asset_id: str,
        service_date: str | None = None,
        description: str | None = None,
        cost: float = 0.0,
        meter_hours_at_service: float = 0.0,
        performed_by: str = "",
    ) -> None:
        """Initializes a MaintenanceLog domain object."""
        self.maintenance_id = maintenance_id
        self.asset_id = asset_id
        self.service_date = service_date
        self.description = description
        self.cost = cost
        self.meter_hours_at_service = meter_hours_at_service
        self.performed_by = performed_by

    # =========================================================================
    # MAGIC METHODS (__repr__, __str__, __eq__, __lt__)
    # =========================================================================

    def __repr__(self) -> str:
        """Returns unambiguous string representation for developer debugging.

        Returns:
            str: Technical representation string.
        """
        return (
            f"MaintenanceLog(maintenance_id='{self.maintenance_id}', "
            f"asset_id='{self.asset_id}', service_date='{self.service_date}', "
            f"cost={self.cost:.2f})"
        )

    def __str__(self) -> str:
        """Returns operator-friendly CLI string summary for maintenance reports.

        Returns:
            str: User-facing CLI string summary.
        """
        return (
            f"[{self.maintenance_id}] Asset: {self.asset_id} | Date: {self.service_date} | "
            f"Meter: {self.meter_hours_at_service} hrs | Cost: ${self.cost:.2f} | Tech: {self.performed_by}"
        )

    def __eq__(self, other: object) -> bool:
        """Compares equality based on unique maintenance_id.

        Args:
            other (object): Object to compare against.

        Returns:
            bool: True if both instances share the same maintenance_id, False otherwise.
        """
        if not isinstance(other, MaintenanceLog):
            return False
        return self.maintenance_id == other.maintenance_id

    def __lt__(self, other: "MaintenanceLog") -> bool:
        """Compares ordering based on service_date and maintenance_id for sorting logs.

        Args:
            other (MaintenanceLog): MaintenanceLog to compare against.

        Returns:
            bool: True if self.service_date < other.service_date (or maintenance_id tie-breaker).
        """
        if not isinstance(other, MaintenanceLog):
            return NotImplemented
        date_self = self.service_date or ""
        date_other = other.service_date or ""
        if date_self == date_other:
            return (self.maintenance_id or "") < (other.maintenance_id or "")
        return date_self < date_other

    # =========================================================================
    # DOMAIN METHODS (Serialization Stubs)
    # =========================================================================

    def to_dict(self) -> dict:
        """Serializes maintenance log object to a dictionary for JSON storage.

        Returns:
            dict: Dictionary representation matching storage/maintenance.json schema.
        """
        return {
            "maintenance_id": self.maintenance_id,
            "asset_id": self.asset_id,
            "service_date": self.service_date,
            "description": self.description,
            "cost": self.cost,
            "meter_hours_at_service": self.meter_hours_at_service,
            "performed_by": self.performed_by,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MaintenanceLog":
        """Deserializes a dictionary record into a MaintenanceLog domain object.

        Args:
            data (dict): Raw dictionary from JSON storage.

        Returns:
            MaintenanceLog: Hydrated MaintenanceLog domain instance.
        """
        return cls(
            maintenance_id=data["maintenance_id"],
            asset_id=data["asset_id"],
            service_date=data["service_date"],
            description=data["description"],
            cost=data["cost"],
            meter_hours_at_service=data["meter_hours_at_service"],
            performed_by=data["performed_by"],
        )


     # =========================================================================
    # Setters and Getters
    # =========================================================================

    @property
    def cost(self) -> float:
        return self._cost

    @cost.setter
    def cost(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Cost must be a non-negative number.")
        self._cost = float(value)
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Description must be a non-empty string.")
        self._description = value.strip()
    
    @property 
    def service_date(self) -> str:
        return self._service_date
    
    @service_date.setter
    def service_date(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Service date must be a non-empty string.")
        self._service_date = value.strip()
    
    @property 
    def perform_by(self) -> str: 
        return self._performed_by
    
    @perform_by.setter
    def perform_by(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Performed by must be a non-empty string.")
        self._performed_by = value.strip()
        
    
