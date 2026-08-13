from datetime import datetime, timedelta
import random

from models.contract_model.contract import Contract
from models.fleet_management_models import PoweredEquipment
from repositories.json_repository import JSONRepository
from services.customer_service import CustomerService
from services.fleet_service import FleetService
from utils.validators import validate_unique_ids

def get_end_date_using_duration_date(duration_days: int) -> str:
    """Calculates planned return end date string from duration days."""
    end_date = datetime.now() + timedelta(days=duration_days)
    return end_date.strftime("%Y-%m-%d")

def contract_id_generator() -> str:
    """Generates a random unique contract ID tag (e.g., 'CNTR-5421')."""
    return f"CNTR-{random.randint(5000, 9999)}"

class RentalService:
    def __init__(
        self,
        contract_repository: JSONRepository,
        fleet_service: FleetService,
        customer_service: CustomerService,
    ) -> None:
        """Initializes RentalService with injected service dependencies and storage repository."""
        self.contract_repository = contract_repository
        self.fleet_service = fleet_service
        self.customer_service = customer_service
        self.contract_list: list[Contract] = []
        self._load_contract_cache()

    def _load_contract_cache(self) -> None:
        """Loads raw JSON dictionaries into Contract object instances in memory."""
        for contract in self.contract_repository.load_all():
            each_contract = Contract.from_dict(contract)
            self.contract_list.append(each_contract)

    def save_contract_cache(self) -> None:
        """Serializes Contract objects back to JSON disk storage."""
        serialized_data = [item.to_dict() for item in self.contract_list]
        self.contract_repository.save_all(serialized_data)

    def get_contract_by_id(self, contract_id: str) -> Contract:
        for contract in self.contract_list:
            if contract_id == contract.contract_id:
                return contract
        raise ValueError(f"Contract with ID '{contract_id}' was not found.")

    def get_active_contracts(self) -> list[Contract]:
        """Returns a list of all currently active rental contracts.

        Returns:
            list[Contract]: List of active Contract objects in memory.
        """
        return [contract for contract in self.contract_list if contract.status == "ACTIVE"]

    def get_active_contract(self) -> list[Contract]:
        """Alias for get_active_contracts."""
        return self.get_active_contracts()

    def create_contract(self, customer_id: str, asset_id: str, duration_days: int) -> Contract:
        """Dispatches an available equipment asset to an eligible customer and creates a rental contract.

        Args:
            customer_id (str): ID string of customer account initiating rental.
            asset_id (str): Asset tag string of equipment to rent.
            duration_days (int): Rental duration in days.

        Returns:
            Contract: Created and persisted Contract domain object.

        Raises:
            ValueError: If customer or equipment is not found, customer has unpaid balance, or equipment is unavailable.
        """
        # 1. Fetch customer and check credit standing
        customer = self.customer_service.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID '{customer_id}' was not found.")
        if customer.has_unpaid_balance:
            raise ValueError(f"Customer '{customer_id}' has an unpaid balance and is ineligible for new rentals.")

        # 2. Fetch equipment and check availability
        equipment = self.fleet_service.get_equipment_by_id(asset_id)
        if not equipment:
            raise ValueError(f"Equipment asset with ID '{asset_id}' was not found.")

        eq_status = getattr(equipment.status, "value", str(equipment.status)).upper()
        if eq_status != "AVAILABLE":
            raise ValueError(f"Equipment asset '{asset_id}' is currently '{eq_status}' and not AVAILABLE for rental.")

        # 3. Generate unique contract ID
        generate_contract_id = contract_id_generator()
        while not validate_unique_ids(generate_contract_id, self.contract_list):
            generate_contract_id = contract_id_generator()

        # 4. Transition equipment status to RENTED
        equipment.mark_rented()

        # 5. Calculate contract dates and base cost
        start_date_str = datetime.now().strftime("%Y-%m-%d")
        end_date_str = get_end_date_using_duration_date(duration_days)
        daily_rate = getattr(equipment, "daily_rate", 0.0)
        base_cost = daily_rate * duration_days
        initial_hours = getattr(equipment, "current_hours", 0.0)
        fuel_at_dispatch = getattr(equipment, "fuel_level_gal", 0.0)

        if not customer.customer_id:
            raise ValueError(f"Customer '{customer_id}' is missing a valid customer_id.")

        if not equipment.asset_id:
            raise ValueError(f"Equipment '{asset_id}' is missing a valid asset_id.")

        # 6. Instantiate Contract using safe Keyword Arguments
        new_contract = Contract(
            contract_id=generate_contract_id,
            customer_id=customer.customer_id,
            asset_id=equipment.asset_id,
            start_date=start_date_str,
            planned_end_date=end_date_str,
            daily_rate=daily_rate,
            initial_hours=initial_hours,
            fuel_at_dispatch_gal=fuel_at_dispatch,
            base_cost=base_cost,
            status="ACTIVE",
        )

        self.contract_list.append(new_contract)
        self._save_contract_cache()
        return new_contract

    def process_return(
        self,
        contract_id: str,
        return_hours: float,
        fuel_returned_gal: float = 0.0,
        date_returned: str | None = None,
        is_paid: bool = True,
    ) -> Contract:
        actual_date = date_returned or datetime.now().strftime("%Y-%m-%d")
        # Check first if the contract is active or not, return error if not
        contract = self.get_contract_by_id(contract_id)
        if not contract:
            raise ValueError(f"Contract with ID '{contract_id}' was not found.")

        if contract.status != "ACTIVE":
            raise ValueError(f"Contract with ID '{contract_id}' was not Active.")

        # Update the return_hours of the equipment
        equipment = self.fleet_service.get_equipment_by_id(contract.asset_id)
        if not equipment:
            raise ValueError(f"Equipment asset '{contract.asset_id}' not found.")

        # 2. Update engine attributes ONLY if the equipment is powered!
        if isinstance(equipment, PoweredEquipment):
            equipment.current_hours = return_hours
            equipment.current_fuel_gal = fuel_returned_gal

            # 3. Check maintenance threshold using domain method!
            if equipment.requires_service():
                equipment.status = "IN_MAINTENANCE"
            else:
                equipment.status = "AVAILABLE"
        else:
            # Static equipment goes straight back to AVAILABLE!
            equipment.status = "AVAILABLE"

        # Call Close Contract
        contract.close_contract(actual_date, return_hours, fuel_returned_gal)

        # Check Customer if paid or not
        customer = self.customer_service.get_customer_by_id(contract.customer_id)
        if customer and not is_paid:
            customer.flag_delinquent()

        # Save Files
        self._save_contract_cache()
        self.fleet_service.save_equipment_list_to_storage()
        self.customer_service.save_customer_cache()

        return contract





