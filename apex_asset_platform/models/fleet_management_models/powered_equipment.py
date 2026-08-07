from models.fleet_management_models.base_equipment import BaseEquipment, EquipmentType, EquipmentStatus


class PoweredEquipment(BaseEquipment):
    """Specialized domain model representing engine-driven or powered machinery.

    Attributes:
        current_hours (float): Current accumulated operating engine hours.
        hours_at_last_service (float): Hour meter reading at last maintenance.
        service_interval_hours (float): Maximum operating hours allowed between services.
        fuel_capacity_gallons (float): Total fuel tank capacity in gallons.
        current_fuel_gal (float): Current fuel level in gallons.
    """

    def __init__(
        self,
        asset_id: str,
        model_name: str,
        daily_rate: float,
        purchase_year: int,
        status: EquipmentStatus | str = EquipmentStatus.AVAILABLE,
        current_hours: float = 0.0,
        hours_at_last_service: float = 0.0,
        service_interval_hours: float = 100.0,
        fuel_capacity_gallons: float = 0.0,
        current_fuel_gal: float | None = None
    ) -> None:
        """Initializes a PoweredEquipment instance.

        Args:
            asset_id (str): Unique asset tag ID.
            model_name (str): Model description name.
            daily_rate (float): Daily rental charge rate in USD.
            purchase_year (int): Four-digit purchase year.
            status (EquipmentStatus): Operational status enum or string.
            current_hours (float): Initial operating hour meter reading. Defaults to 0.0.
            hours_at_last_service (float): Hour meter reading at last service. Defaults to 0.0.
            service_interval_hours (float): Service threshold interval in hours. Defaults to 100.0.
            fuel_capacity_gallons (float): Fuel tank capacity in gallons. Defaults to 0.0.
            current_fuel_gal (float): Initial fuel level in gallons. Defaults to 0.0.
        """
        super().__init__(asset_id, model_name, daily_rate, purchase_year, status)
        self.equipment_type = EquipmentType.POWERED
        self.current_hours = current_hours
        self.hours_at_last_service = hours_at_last_service
        self.service_interval_hours = service_interval_hours
        self.fuel_capacity_gallons = fuel_capacity_gallons

        if current_fuel_gal is None:
            self.current_fuel_gal = fuel_capacity_gallons
        else:
            self.current_fuel_gal = current_fuel_gal

    @property
    def current_hours(self) -> float:
        """Gets the current_hours meter reading.

        Returns:
            float: Total cumulative engine run-hours.
        """
        return self._current_hours

    @current_hours.setter
    def current_hours(self, value: float) -> None:
        """Sets and validates current_hours.

        Args:
            value (float): Non-negative float or integer hour reading.

        Raises:
            ValueError: If value is negative.
        """
        val = float(value)
        if val < 0:
            raise ValueError("current_hours cannot be negative.")
        self._current_hours = val

    @property
    def hours_at_last_service(self) -> float:
        """Gets the hours_at_last_service.

        Returns:
            float: Hour meter reading at last maintenance.
        """
        return self._hours_at_last_service

    @hours_at_last_service.setter
    def hours_at_last_service(self, value: float) -> None:
        """Sets and validates hours_at_last_service.

        Args:
            value (float): Non-negative float or integer hour reading.

        Raises:
            ValueError: If value is negative.
        """
        val = float(value)
        if val < 0:
            raise ValueError("hours_at_last_service cannot be negative.")
        self._hours_at_last_service = val

    @property
    def service_interval_hours(self) -> float:
        """Gets the service_interval_hours.

        Returns:
            float: Service threshold interval.
        """
        return self._service_interval_hours

    @service_interval_hours.setter
    def service_interval_hours(self, value: float) -> None:
        """Sets and validates service_interval_hours.

        Args:
            value (float): Positive float interval > 0.

        Raises:
            ValueError: If value <= 0.
        """
        val = float(value)
        if val <= 0:
            raise ValueError("service_interval_hours must be greater than 0.")
        self._service_interval_hours = val

    @property
    def fuel_capacity_gallons(self) -> float:
        """Gets the fuel_capacity_gallons.

        Returns:
            float: Tank capacity in gallons.
        """
        return self._fuel_capacity_gallons

    @fuel_capacity_gallons.setter
    def fuel_capacity_gallons(self, value: float) -> None:
        """Sets and validates fuel_capacity_gallons.

        Args:
            value (float): Non-negative tank capacity.

        Raises:
            ValueError: If value is negative.
        """
        val = float(value)
        if val < 0:
            raise ValueError("fuel_capacity_gallons cannot be negative.")
        self._fuel_capacity_gallons = val

    @property
    def current_fuel_gal(self) -> float:
        """Gets the current_fuel_gal.

        Returns:
            float: Current fuel level in gallons.
        """
        return self._current_fuel_gal

    @current_fuel_gal.setter
    def current_fuel_gal(self, value: float) -> None:
        """Sets and validates current_fuel_gal.

        Args:
            value (float): Non-negative fuel level.

        Raises:
            ValueError: If value is negative.
        """
        val = float(value)
        if val < 0:
            raise ValueError("current_fuel_gal cannot be negative.")
        self._current_fuel_gal = val

    def record_usage(self, hours_added: float, fuel_remaining: float) -> None:
        """Records operating usage and updates fuel level upon equipment return.

        Args:
            hours_added (float): Non-negative operating hours to add to meter.
            fuel_remaining (float): Non-negative remaining fuel level in gallons.

        Raises:
            ValueError: If fuel_remaining exceeds tank capacity.
        """
        self.current_hours += hours_added
        if fuel_remaining > self.fuel_capacity_gallons:
            raise ValueError("fuel_remaining cannot be greater than fuel_capacity_gallons.")
        self.current_fuel_gal = fuel_remaining

    def requires_service(self) -> bool:
        """Evaluates whether operating hours have reached or passed the service threshold.

        Returns:
            bool: True if (current_hours - hours_at_last_service) >= service_interval_hours, False otherwise.
        """
        return self.current_hours - self.hours_at_last_service >= self.service_interval_hours

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

    def to_dict(self) -> dict:
        """Serializes powered equipment attributes to a dictionary for JSON persistence.

        Returns:
            dict: Dictionary representation of powered equipment attributes.
        """
        data = super().to_dict()
        data['current_hours'] = self.current_hours
        data['hours_at_last_service'] = self.hours_at_last_service
        data['service_interval_hours'] = self.service_interval_hours
        data['fuel_capacity_gal'] = self.fuel_capacity_gallons
        data['current_fuel_gal'] = self.current_fuel_gal
        return data
