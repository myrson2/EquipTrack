from typing import Any


class Contract:
    """Domain model representing a binding rental agreement between a customer and an equipment asset.

    Attributes:
        contract_id (str): Unique contract identification tag (e.g., 'CNTR-2001').
        customer_id (str): Associated customer account ID (e.g., 'CUST-5001').
        asset_id (str): Rented equipment asset tag ID (e.g., 'EQ-1001').
        start_date (str): Rental agreement start date (YYYY-MM-DD).
        planned_end_date (str): Expected rental end date (YYYY-MM-DD).
        actual_return_date (str | None): Date equipment was returned (YYYY-MM-DD), or None if active.
        initial_hours (float): Engine hour-meter reading at dispatch.
        return_hours (float | None): Engine hour-meter reading at return, or None if active.
        fuel_at_dispatch_gal (float): Tank fuel capacity / fuel level at dispatch in gallons.
        fuel_returned_gal (float | None): Tank fuel level at return in gallons, or None if active.
        daily_rate (float): Agreed daily rental rate in USD.
        base_cost (float): Initial base rental cost calculated at dispatch.
        penalty_fees (float): Accrued overdue and refueling penalty fees.
        status (str): Current contract status ('ACTIVE', 'CLOSED', 'CANCELLED').
    """

    def __init__(
        self,
        customer_id: str,
        asset_id: str,
        start_date: str,
        planned_end_date: str,
        daily_rate: float = 0.0,
        initial_hours: float = 0.0,
        fuel_at_dispatch_gal: float = 0.0,
        contract_id: str = "PENDING",
        actual_return_date: str | None = None,
        return_hours: float | None = None,
        fuel_returned_gal: float | None = None,
        base_cost: float = 0.0,
        penalty_fees: float = 0.0,
        status: str = "ACTIVE",
    ) -> None:
        """Initializes a Contract instance.

        Args:
            customer_id (str): Unique customer account ID.
            asset_id (str): Rented equipment asset tag ID.
            start_date (str): Start date string (YYYY-MM-DD).
            planned_end_date (str): Planned return date string (YYYY-MM-DD).
            daily_rate (float, optional): Agreed daily rental rate in USD. Defaults to 0.0.
            initial_hours (float, optional): Dispatch hour-meter reading. Defaults to 0.0.
            fuel_at_dispatch_gal (float, optional): Dispatch fuel level in gallons. Defaults to 0.0.
            contract_id (str, optional): Unique contract ID tag. Defaults to 'PENDING'.
            actual_return_date (str | None, optional): Actual return date. Defaults to None.
            return_hours (float | None, optional): Return hour-meter reading. Defaults to None.
            fuel_returned_gal (float | None, optional): Return fuel level in gallons. Defaults to None.
            base_cost (float, optional): Calculated base rental cost. Defaults to 0.0.
            penalty_fees (float, optional): Calculated penalty fees. Defaults to 0.0.
            status (str, optional): Contract status ('ACTIVE', 'CLOSED', 'CANCELLED'). Defaults to 'ACTIVE'.
        """
        self.contract_id = contract_id
        self.customer_id = customer_id
        self.asset_id = asset_id
        self.start_date = start_date
        self.planned_end_date = planned_end_date
        self.actual_return_date = actual_return_date
        self.initial_hours = initial_hours
        self.return_hours = return_hours
        self.fuel_at_dispatch_gal = fuel_at_dispatch_gal
        self.fuel_returned_gal = fuel_returned_gal
        self.daily_rate = daily_rate
        self.base_cost = base_cost
        self.penalty_fees = penalty_fees
        self.status = status

    @property
    def contract_id(self) -> str:
        """Gets unique contract identification tag.

        Returns:
            str: Contract ID.
        """
        return self._contract_id

    @contract_id.setter
    def contract_id(self, value: str) -> None:
        """Sets contract identification tag with non-empty string validation.

        Args:
            value (str): Contract ID string.

        Raises:
            ValueError: If contract ID is empty or invalid.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Contract ID must be a non-empty string.")
        self._contract_id = value.strip()

    @property
    def customer_id(self) -> str:
        """Gets customer identification tag.

        Returns:
            str: Customer ID.
        """
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value: str) -> None:
        """Sets customer identification tag with non-empty string validation.

        Args:
            value (str): Customer ID string.

        Raises:
            ValueError: If customer ID is empty or invalid.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Customer ID must be a non-empty string.")
        self._customer_id = value.strip()

    @property
    def asset_id(self) -> str:
        """Gets rented equipment asset tag ID.

        Returns:
            str: Equipment asset ID.
        """
        return self._asset_id

    @asset_id.setter
    def asset_id(self, value: str) -> None:
        """Sets equipment asset tag ID with non-empty string validation.

        Args:
            value (str): Equipment asset ID string.

        Raises:
            ValueError: If asset ID is empty or invalid.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Asset ID must be a non-empty string.")
        self._asset_id = value.strip()

    @property
    def start_date(self) -> str:
        """Gets contract start date string.

        Returns:
            str: Start date (YYYY-MM-DD).
        """
        return self._start_date

    @start_date.setter
    def start_date(self, value: str) -> None:
        """Sets contract start date with non-empty validation.

        Args:
            value (str): Start date string.

        Raises:
            ValueError: If start date is empty.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Start date must be a non-empty string.")
        self._start_date = value.strip()

    @property
    def planned_end_date(self) -> str:
        """Gets planned return date string.

        Returns:
            str: Planned end date (YYYY-MM-DD).
        """
        return self._planned_end_date

    @planned_end_date.setter
    def planned_end_date(self, value: str) -> None:
        """Sets planned return date with non-empty validation.

        Args:
            value (str): Planned end date string.

        Raises:
            ValueError: If planned end date is empty.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Planned end date must be a non-empty string.")
        self._planned_end_date = value.strip()

    @property
    def actual_return_date(self) -> str | None:
        """Gets actual return date string.

        Returns:
            str | None: Actual return date or None if active.
        """
        return self._actual_return_date

    @actual_return_date.setter
    def actual_return_date(self, value: str | None) -> None:
        """Sets actual return date.

        Args:
            value (str | None): Actual return date string or None.
        """
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError("Actual return date must be a string or None.")
        self._actual_return_date = value.strip() if value else None

    @property
    def initial_hours(self) -> float:
        """Gets dispatch hour-meter reading.

        Returns:
            float: Starting run hours.
        """
        return self._initial_hours

    @initial_hours.setter
    def initial_hours(self, value: float) -> None:
        """Sets dispatch hour-meter reading with non-negative validation.

        Args:
            value (float): Starting run hours.

        Raises:
            ValueError: If initial hours is negative.
        """
        val = float(value)
        if val < 0:
            raise ValueError("Initial hours cannot be negative.")
        self._initial_hours = val

    @property
    def return_hours(self) -> float | None:
        """Gets return hour-meter reading.

        Returns:
            float | None: Return run hours or None if active.
        """
        return self._return_hours

    @return_hours.setter
    def return_hours(self, value: float | None) -> None:
        """Sets return hour-meter reading with non-negative validation.

        Args:
            value (float | None): Return run hours or None.

        Raises:
            ValueError: If return hours is negative.
        """
        if value is None or str(value).strip() == "":
            self._return_hours = None
        else:
            val = float(value)
            if val < 0:
                raise ValueError("Return hours cannot be negative.")
            self._return_hours = val

    @property
    def fuel_at_dispatch_gal(self) -> float:
        """Gets dispatch fuel level in gallons.

        Returns:
            float: Dispatch fuel level.
        """
        return self._fuel_at_dispatch_gal

    @fuel_at_dispatch_gal.setter
    def fuel_at_dispatch_gal(self, value: float) -> None:
        """Sets dispatch fuel level with non-negative validation.

        Args:
            value (float): Dispatch fuel level in gallons.

        Raises:
            ValueError: If fuel level is negative.
        """
        val = float(value)
        if val < 0:
            raise ValueError("Dispatch fuel level cannot be negative.")
        self._fuel_at_dispatch_gal = val

    @property
    def fuel_returned_gal(self) -> float | None:
        """Gets return fuel level in gallons.

        Returns:
            float | None: Return fuel level or None if active.
        """
        return self._fuel_returned_gal

    @fuel_returned_gal.setter
    def fuel_returned_gal(self, value: float | None) -> None:
        """Sets return fuel level with non-negative validation.

        Args:
            value (float | None): Return fuel level in gallons or None.

        Raises:
            ValueError: If fuel level is negative.
        """
        if value is None or str(value).strip() == "":
            self._fuel_returned_gal = None
        else:
            val = float(value)
            if val < 0:
                raise ValueError("Returned fuel level cannot be negative.")
            self._fuel_returned_gal = val

    @property
    def daily_rate(self) -> float:
        """Gets agreed daily rental rate in USD.

        Returns:
            float: Daily rental rate.
        """
        return self._daily_rate

    @daily_rate.setter
    def daily_rate(self, value: float) -> None:
        """Sets agreed daily rental rate with non-negative validation.

        Args:
            value (float): Daily rental rate.

        Raises:
            ValueError: If daily rate is negative.
        """
        val = float(value)
        if val < 0:
            raise ValueError("Daily rate cannot be negative.")
        self._daily_rate = val

    @property
    def base_cost(self) -> float:
        """Gets base rental cost.

        Returns:
            float: Base cost in USD.
        """
        return self._base_cost

    @base_cost.setter
    def base_cost(self, value: float) -> None:
        """Sets base rental cost with non-negative validation.

        Args:
            value (float): Base cost in USD.

        Raises:
            ValueError: If base cost is negative.
        """
        val = float(value)
        if val < 0:
            raise ValueError("Base cost cannot be negative.")
        self._base_cost = val

    @property
    def penalty_fees(self) -> float:
        """Gets total penalty fees.

        Returns:
            float: Penalty fees in USD.
        """
        return self._penalty_fees

    @penalty_fees.setter
    def penalty_fees(self, value: float) -> None:
        """Sets total penalty fees with non-negative validation.

        Args:
            value (float): Penalty fees in USD.

        Raises:
            ValueError: If penalty fees is negative.
        """
        val = float(value)
        if val < 0:
            raise ValueError("Penalty fees cannot be negative.")
        self._penalty_fees = val

    @property
    def status(self) -> str:
        """Gets contract operational status.

        Returns:
            str: Status string ('ACTIVE', 'CLOSED', 'CANCELLED').
        """
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Sets contract status with valid state choice validation.

        Args:
            value (str): Status string ('ACTIVE', 'CLOSED', 'CANCELLED').

        Raises:
            ValueError: If status is not one of valid states.
        """
        valid_statuses = {"ACTIVE", "CLOSED", "CANCELLED"}
        val = value.strip().upper()
        if val not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}.")
        self._status = val

    def calculate_overdue_days(self, return_date_str: str | None = None) -> int:
        """Calculates overdue days beyond planned_end_date.

        Args:
            return_date_str (str | None, optional): Actual return date string (YYYY-MM-DD). Defaults to None.

        Returns:
            int: Number of overdue days (0 if returned on time or early).
        """
        pass

    def close_contract(
        self,
        actual_return_date: str,
        return_hours: float,
        fuel_returned_gal: float = 0.0,
        fuel_fee_per_gal: float = 5.0,
    ) -> None:
        """Closes contract, calculates overdue days, refueling fees, and updates status to CLOSED.

        Args:
            actual_return_date (str): Actual return date string (YYYY-MM-DD).
            return_hours (float): Engine hour-meter reading at return.
            fuel_returned_gal (float, optional): Gallons of fuel in tank at return. Defaults to 0.0.
            fuel_fee_per_gal (float, optional): Refueling surcharge fee per missing gallon. Defaults to 5.0.
        """
        pass

    def to_dict(self) -> dict[str, Any]:
        """Serializes contract attributes into a JSON-compatible dictionary.

        Returns:
            dict[str, Any]: Dictionary containing contract fields.
        """
        pass

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Contract":
        """Instantiates a Contract model instance from a dictionary record.

        Args:
            data (dict[str, Any]): Dictionary containing contract fields.

        Returns:
            Contract: Reconstructed Contract model instance.
        """
        pass

    def __repr__(self) -> str:
        """Returns string representation for developers.

        Returns:
            str: Developer representation of Contract instance.
        """
        return (
            f"{self.__class__.__name__}(contract_id='{self.contract_id}', "
            f"customer_id='{self.customer_id}', asset_id='{self.asset_id}', status='{self.status}')"
        )

    def __str__(self) -> str:
        """Returns operator-friendly CLI string representation.

        Returns:
            str: User-facing CLI string summary.
        """
        ret_date = self.actual_return_date or "Active (On Rent)"
        total_due = self.base_cost + self.penalty_fees
        return (
            f"[{self.contract_id}] Customer: {self.customer_id} | Asset: {self.asset_id} | "
            f"Dates: {self.start_date} to {self.planned_end_date} (Return: {ret_date}) | "
            f"Base: ${self.base_cost:.2f} | Fees: ${self.penalty_fees:.2f} | Total: ${total_due:.2f} | Status: {self.status}"
        )

    def __eq__(self, other: object) -> bool:
        """Checks equality between two Contract instances based on contract_id.

        Args:
            other (object): Other object to compare against.

        Returns:
            bool: True if both instances share the same contract_id.
        """
        if not isinstance(other, Contract):
            return False
        return self.contract_id == other.contract_id
