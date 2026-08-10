import random
from typing import Any
from models.customer_model.customer import Customer
from repositories.json_repository import JSONRepository
from utils.validators import gmail_validator, phone_validator, validate_unique_ids
1

def customer_id_generator() -> str:
    """Generates a random customer ID.
    Returns:
    """
    return "CUST-{}".format(random.randint(5000,  6000))

class CustomerService:
    """Service layer orchestrating customer account operations and persistence.

    Attributes:
        customer_repository (JSONRepository): JSON repository managing storage/customers.json.
        customer_list (list[Customer]): In-memory list cache of Customer instances.
    """

    def __init__(self, customer_repository: JSONRepository) -> None:
        """Initializes CustomerService with a JSON repository dependency.

        Args:
            customer_repository (JSONRepository): Repository instance bound to storage/customers.json.
        """
        self.customer_repository = customer_repository
        self.customer_list: list[Customer] = []
        self._load_customer_cache()

    def _load_customer_cache(self) -> None:
        """Loads raw JSON dictionaries into Customer object instances in memory."""
        for customer in self.customer_repository.load_all():
            each_cust = Customer.from_dict(customer)
            self.customer_list.append(each_cust)

    def _save_customer_cache(self) -> None:
        """Serializes in-memory Customer object instances back to JSON disk storage."""
        serialized_data = [item.to_dict() for item in self.customer_list]
        self.customer_repository.save_all(serialized_data)
        pass

    def register_customer(self, customer: Customer) -> None:
        """Registers a new customer account, enforcing email/phone format guardrails,
        intercepting duplicate IDs/emails, and persisting to disk.

        Args:
            customer (Customer): Customer instance to add.

        Raises:
            ValueError: If email is missing @gmail.com, phone doesn't start with 09 (11 digits), or duplicate exists.
        """
        # Guardrail 1: Email domain must be @gmail.com
        if not gmail_validator(customer.email):
            raise ValueError("Invalid email format. Must be a valid '@gmail.com' address.")

        # Guardrail 2: Phone must start with '09', contain digits only, and be 11 digits long
        if not phone_validator(customer.phone):
            raise ValueError("Invalid phone number. Must start with '09' and be exactly 11 digits long.")

        # Guardrail 3: Duplicate email check
        if any(c.email.lower() == customer.email.lower() for c in self.customer_list):
            raise ValueError(f"Customer with email '{customer.email}' is already registered.")

        # Generate unique Customer ID and save to storage
        generated_id = customer_id_generator()
        if validate_unique_ids(generated_id, self.customer_list):
            customer.customer_id = generated_id
            self.customer_list.append(customer)
            self._save_customer_cache()
        else:
            raise ValueError(f"Customer with ID '{generated_id}' already exists.")

    def get_all_customers(self) -> list[Customer]:
        """Returns all registered customer accounts.

        Returns:
            list[Customer]: List of all Customer objects in memory sorted by customer_id.
        """
        return sorted(self.customer_list, key=lambda c: c.customer_id)

    def get_customer_by_id(self, customer_id: str) -> Customer:
        """Looks up a customer account by unique ID tag.

        Args:
            customer_id (str): Unique customer ID tag.

        Returns:
            Customer: Matching Customer object.

        Raises:
            ValueError: If no customer matching the ID is found.
        """
        for customer in self.customer_list:
            if customer.customer_id == customer_id.strip():
                return customer
        raise ValueError(f"Customer with ID '{customer_id}' does not exist.")

    def search_customers(self, query: str) -> list[Customer]:
        """Searches customer accounts by company name or customer ID keyword.

        Args:
            query (str): Search keyword.

        Returns:
            list[Customer]: List of matching Customer objects.
        """
        clean_query = query.strip().lower()
        return [
            c
            for c in self.customer_list
            if clean_query in c.company_name.lower()
            or clean_query in c.customer_id.lower()
        ]

    def get_unpaid_customers(self) -> list[Customer]:
        return [customer for customer in self.customer_list if customer.has_unpaid_balance]

    def get_paid_customers(self) -> list[Customer]:
        return [customer for customer in self.customer_list if not customer.has_unpaid_balance]


    def update_credit_status(
        self, customer_id: str, possesses_unpaid_balance: bool
    ) -> Customer:
        """Updates delinquency standing for a customer account and persists state to disk.

        Args:
            customer_id (str): Unique customer ID tag.
            possesses_unpaid_balance (bool): True if delinquent/unpaid, False if paid.

        Returns:
            Customer: Updated Customer object instance.
        """
        customer = self.get_customer_by_id(customer_id)
        if possesses_unpaid_balance:
            customer.flag_delinquent()
        else:
            customer.clear_delinquent()

        self._save_customer_cache()
        return customer
