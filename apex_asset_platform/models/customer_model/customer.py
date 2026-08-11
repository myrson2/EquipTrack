from typing import Any


class Customer:
    """Domain model representing a business client registered for equipment rentals.

    Attributes:
        customer_id (str): Unique customer identification tag (e.g., 'CUST-1001').
        company_name (str): Legal business name of the client firm.
        email (str): Primary contact email address.
        phone (str): Primary contact phone number.
        has_unpaid_balance (bool): Flag indicating if the account has outstanding unpaid bills.
    """

    def __init__(
        self,
        company_name: str,
        email: str,
        phone: str,
        has_unpaid_balance: bool = True,
        customer_id: str | None = None,
    ) -> None:
        """Initializes a Customer instance.

        Args:
            customer_id (str): Unique customer ID string.
            company_name (str): Company name string.
            email (str): Primary contact email string.
            phone (str): Primary contact phone number string.
            has_unpaid_balance (bool, optional): Unpaid balance delinquency status. Defaults to False.
        """
        self.customer_id = customer_id
        self.company_name = company_name
        self.email = email
        self.phone = phone
        self.has_unpaid_balance = has_unpaid_balance

    @property
    def company_name(self) -> str:
        """Gets the company name.

        Returns:
            str: Registered company name.
        """
        return self._company_name

    @company_name.setter
    def company_name(self, value: str) -> None:
        """Sets the company name with non-empty string validation.

        Args:
            value (str): Company name string.

        Raises:
            ValueError: If company name is empty or invalid.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Company name must be a non-empty string.")
        self._company_name = value.strip()

    @property
    def email(self) -> str:
        """Gets the contact email address.

        Returns:
            str: Contact email.
        """
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Sets the contact email address with @gmail.com validation.

        Args:
            value (str): Email address string.

        Raises:
            ValueError: If email is empty, missing '@', or not a @gmail.com address.
        """
        if not isinstance(value, str) or "@" not in value or not value.strip():
            raise ValueError("Invalid email format. Must be a valid email address.")
        self._email = value.strip()

    @property
    def phone(self) -> str:
        """Gets the contact phone number.

        Returns:
            str: Phone number.
        """
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        """Sets the contact phone number with non-empty validation.

        Args:
            value (str): Phone number string.

        Raises:
            ValueError: If phone number is empty or invalid.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Phone number must be a non-empty string.")
        self._phone = value.strip()

    @property
    def has_unpaid_balance(self) -> bool:
        """Gets delinquency balance flag.

        Returns:
            bool: True if account has an unpaid balance, False otherwise.
        """
        return self._has_unpaid_balance

    @has_unpaid_balance.setter
    def has_unpaid_balance(self, value: bool) -> None:
        """Sets the delinquency balance flag.

        Args:
            value (bool): Boolean flag indicating unpaid status.
        """
        self._has_unpaid_balance = bool(value)

    def flag_delinquent(self) -> None:
        """Flags the customer account as delinquent due to unpaid balances."""
        self.has_unpaid_balance = True

    def clear_delinquent(self) -> None:
        """Clears delinquency flag on the customer account."""
        self.has_unpaid_balance = False

    def to_dict(self) -> dict:
        """Serializes customer model attributes to a JSON-compatible dictionary.

        Returns:
            dict[str, Any]: Dictionary containing customer record fields.
        """
        return {
            "customer_id": self.customer_id,
            "company_name": self.company_name,
            "email": self.email,
            "phone": self.phone,
            "has_unpaid_balance": self.has_unpaid_balance,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Customer":
        """Instantiates a Customer model instance from a dictionary record.

        Args:
            data (dict[str, Any]): Dictionary containing customer record fields.

        Returns:
            Customer: Reconstructed Customer model instance.
        """
        raw_unpaid = data.get("has_unpaid_balance", False)
        has_unpaid = (
            raw_unpaid.strip().lower() == "true"
            if isinstance(raw_unpaid, str)
            else bool(raw_unpaid)
        )

        return cls(
            customer_id=data["customer_id"],
            company_name=data["company_name"],
            email=data["email"],
            phone=data["phone"],
            has_unpaid_balance=has_unpaid,
        )

    def __repr__(self) -> str:
        """Returns string representation for developers.

        Returns:
            str: Developer representation of Customer instance.
        """
        return (
            f"{self.__class__.__name__}(customer_id='{self.customer_id}', "
            f"company_name='{self.company_name}', has_unpaid_balance={self.has_unpaid_balance})"
        )

    def __str__(self) -> str:
        """Returns operator-friendly CLI string representation.

        Returns:
            str: User-facing CLI string summary.
        """
        standing = "DELINQUENT (Unpaid Balance)" if self.has_unpaid_balance else "Good Standing"
        return f"[{self.customer_id}] {self.company_name} | Contact: {self.email} ({self.phone}) | Status: {standing}"

    def __eq__(self, other: object) -> bool:
        """Checks equality between two Customer instances based on unique customer_id.

        Args:
            other (object): Other object to compare against.

        Returns:
            bool: True if both instances share the same customer_id.
        """
        if not isinstance(other, Customer):
            return False
        return self.customer_id == other.customer_id

    def __lt__(self, other: object) -> bool:
        """Compares two Customer instances by customer_id for
            sorting."""
        if not isinstance(other, Customer):
            return NotImplemented
        return self.customer_id < other.customer_id
