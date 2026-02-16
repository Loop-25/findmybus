from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class ServiceType(str, Enum):
    FUEL = "fuel"
    GROCERIES = "groceries"
    FOOD = "food"
    MOTOCAB = "motocab"


class OrderStatus(str, Enum):
    CREATED = "created"
    PRICED = "priced"
    DRIVER_ASSIGNED = "driver_assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Location:
    latitude: float
    longitude: float


@dataclass
class DeliveryItem:
    name: str
    quantity: float
    unit_price: float


@dataclass
class CustomerOrder:
    id: str
    customer_id: str
    service_type: ServiceType
    pickup: Location
    dropoff: Location
    distance_km: float
    items: List[DeliveryItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    metadata: Dict[str, str] = field(default_factory=dict)
    assigned_driver_id: Optional[str] = None

    @property
    def basket_total(self) -> float:
        return round(sum(item.quantity * item.unit_price for item in self.items), 2)


@dataclass
class Driver:
    id: str
    service_type: ServiceType
    current_location: Location
    is_available: bool = True


@dataclass
class PriceBreakdown:
    base_fee: float
    distance_fee: float
    service_fee: float
    surge_multiplier: float

    @property
    def total(self) -> float:
        raw_total = (self.base_fee + self.distance_fee + self.service_fee) * self.surge_multiplier
        return round(raw_total, 2)
