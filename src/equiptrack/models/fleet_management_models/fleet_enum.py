from enum import Enum

class EquipmentType(Enum):
    POWERED = 'POWERED'
    STATIC = 'STATIC'

class EquipmentStatus(Enum):
    AVAILABLE = 'AVAILABLE'
    IN_MAINTENANCE = 'IN_MAINTENANCE'
    RENTED = 'RENTED'