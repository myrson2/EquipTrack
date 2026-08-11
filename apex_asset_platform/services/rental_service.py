from models.contract_model.contract import Contract
from repositories.json_repository import JSONRepository

class RentalService:
    def __init__(self, contract_repository: JSONRepository):
        self.contract_repository = contract_repository
        self.contract_list: list[Contract] = []
        self._load_contract_cache()

    def _load_contract_cache(self) -> None:
        for contract in self.contract_repository.load_all():
            each_contract = Contract.from_dict()
            self.contract_list.append(each_contract)

    def _save_contract_cache(self) -> None:
        serialized_data = [item.to_dict() for item in self.contract_list]
        self.contract_repository.save_all(serialized_data)