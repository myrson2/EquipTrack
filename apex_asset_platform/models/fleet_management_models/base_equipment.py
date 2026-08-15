from enum import Enum
from models.fleet_management_models.fleet_enum import EquipmentType, EquipmentStatus

class BaseEquipment:
    """Base domain model representing a generic piece of fleet equipment.

    Attributes:
        asset_id (str): Unique identifier for the equipment asset.
        equipment_type (EquipmentType): Category flag (STATIC or POWERED).
        model_name (str): Descriptive model name.
        daily_rate (float): Base daily rental rate in USD.
        purchase_year (int): Year the machinery was acquired.
        status (EquipmentStatus): Current operational status (AVAILABLE, IN_MAINTENANCE, RENTED).
    """

    def __init__(
        self,
        model_name: str,
        daily_rate: float,
        purchase_year: int,
        equipment_type: EquipmentType | str = EquipmentType.STATIC,
        status: EquipmentStatus | str = EquipmentStatus.AVAILABLE,
        asset_id: str | None = None,
    ) -> None:
        """Initializes a BaseEquipment instance.

        Args:
            asset_id (str): Unique asset tag ID (e.g., 'EQ-1001').
            model_name (str): Model name description.
            daily_rate (float): Non-negative daily rental charge.
            purchase_year (int): Four-digit purchase year.
            status (EquipmentStatus): Operational status enum or string.
        """

        self.asset_id = asset_id
        self.equipment_type = equipment_type
        self.model_name = model_name
        self.daily_rate = daily_rate
        self.purchase_year = purchase_year
        self.status = status

    def __repr__(self) -> str:
        """Returns string representation for developers.
1
        Returns:
            str: Developer-focused string representation of the BaseEquipment.
        """
        status_str = self.status.value if isinstance(self.status, Enum) else self.status
        return f"{self.__class__.__name__}(asset_id='{self.asset_id}', model_name='{self.model_name}', status='{status_str}')"

    def __str__(self) -> str:
        """Returns operator-friendly string representation.

        Returns:
            str: User-facing CLI string summary.
        """
        status_str = self.status.value if isinstance(self.status, Enum) else self.status
        return f"[{self.asset_id}] {self.model_name} ({status_str}) - ${self.daily_rate:.2f}/day"

    def __eq__(self, other: object) -> bool:
        """Compares equality based on unique asset_id.

        Args:
            other (object): Another object instance to compare.

        Returns:
            bool: True if both instances share the same asset_id, False otherwise.
        """
        if not isinstance(other, BaseEquipment):
            return False
        return self.asset_id == other.asset_id

    def __lt__(self, other: "BaseEquipment") -> bool:
        """Compares asset_id ordering for sorting collections.

        Args:
            other (BaseEquipment): Target equipment to compare against.

        Returns:
            bool: True if self.asset_id < other.asset_id.
        """
        if not isinstance(other, BaseEquipment):
            return NotImplemented
        id_self = self.asset_id or ""
        id_other = other.asset_id or ""
        return id_self < id_other

    @property
    def asset_id(self) -> str:
        """Gets the asset_id.
    
        Returns:
            str: Unique asset ID string.
        """
        return self._asset_id
    
    @asset_id.setter
    def asset_id(self, value: str | None) -> None:
        """Sets and validates the asset_id.

        Args:
            value (str | None): Non-empty string asset ID or None during initial drafting.

        Raises:
            ValueError: If value is empty string or not a string.
        """
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError("asset_id must be a non-empty string.")
        self._asset_id = value.strip() if value else None

    @property
    def equipment_type(self) -> EquipmentType:
        """Gets the equipment_type.

        Returns:
            EquipmentType: Category enum.
        """
        return self._equipment_type

    @equipment_type.setter
    def equipment_type(self, value: EquipmentType | str) -> None:
        """Sets and converts the equipment_type.

        Args:
            value (EquipmentType | str): Enum or string name.
        """
        if isinstance(value, str):
            value = EquipmentType(value)
        self._equipment_type = value

    @property
    def model_name(self) -> str:
        """Gets the model_name.

        Returns:
            str: Model name description.
        """
        return self._model_name

    @model_name.setter
    def model_name(self, value: str) -> None:
        """Sets and validates the model_name.

        Args:
            value (str): Non-empty string model name.

        Raises:
            ValueError: If value is empty or not a string.
        """
        if not value or not isinstance(value, str):
            raise ValueError("model_name must be a non-empty string.")
        self._model_name = value

    @property
    def daily_rate(self) -> float:
        """Gets the daily_rate.

        Returns:
            float: Daily rental rate in USD.
        """
        return self._daily_rate

    @daily_rate.setter
    def daily_rate(self, value: float) -> None:
        """Sets and validates the daily_rate.

        Args:
            value (float): Non-negative float or integer.

        Raises:
            ValueError: If value is negative.
        """
        val = float(value)
        if val < 0:
            raise ValueError("daily_rate cannot be negative.")
        self._daily_rate = val

    @property
    def purchase_year(self) -> int:
        """Gets the purchase_year.

        Returns:
            int: Purchase year.
        """
        return self._purchase_year

    @purchase_year.setter
    def purchase_year(self, value: int) -> None:
        """Sets and validates the purchase_year.

        Args:
            value (int): Positive four-digit integer year.

        Raises:
            ValueError: If value is less than or equal to zero.
        """
        val = int(value)
        if val <= 0:
            raise ValueError("purchase_year must be a positive integer.")
        self._purchase_year = val

    @property
    def status(self) -> EquipmentStatus:
        """Gets the operational status.

        Returns:
            EquipmentStatus: Current status enum.
        """
        return self._status

    @status.setter
    def status(self, value: EquipmentStatus | str) -> None:
        """Sets and converts the operational status.

        Args:
            value (EquipmentStatus | str): Status enum or string.
        """
        if isinstance(value, str):
            value = EquipmentStatus(value)
        self._status = value

    def calculate_rental_cost(self, days: int) -> float:
        """Calculates total base rental cost for a specified duration.

        Args:
            days (int): Rental duration in days (must be > 0).

        Returns:
            float: Total calculated rental charge in USD.

        Raises:
            ValueError: If days <= 0.
        """
        if days <= 0:
            raise ValueError("Rental duration days must be greater than 0.")
        return days * self.daily_rate

    def mark_maintenance(self) -> None:
        """Updates the operational status to IN_MAINTENANCE."""
        self.status = EquipmentStatus.IN_MAINTENANCE

    def mark_available(self) -> None:
        """Updates the operational status to AVAILABLE."""
        self.status = EquipmentStatus.AVAILABLE

    def mark_rented(self) -> None:
        """Updates the operational status to RENT."""
        self.status = EquipmentStatus.RENTED

    def to_dict(self) -> dict:
        """Serializes the equipment object to a dictionary for JSON persistence.

        Returns:
            dict: Dictionary representation of the equipment attributes.
        """
        return {
            "asset_id": self.asset_id,
            "equipment_type": self.equipment_type.value if isinstance(self.equipment_type, Enum) else self.equipment_type,
            "model_name": self.model_name,
            "daily_rate": self.daily_rate,
            "purchase_year": self.purchase_year,
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
        }