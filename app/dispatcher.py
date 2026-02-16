from __future__ import annotations

from typing import Iterable, Optional

from app.domain import CustomerOrder, Driver, OrderStatus


def assign_driver(order: CustomerOrder, drivers: Iterable[Driver]) -> Optional[Driver]:
    """Assign the closest available driver for the order service type."""
    available = [d for d in drivers if d.service_type == order.service_type and d.is_available]
    if not available:
        return None

    def distance_score(driver: Driver) -> float:
        lat_delta = order.pickup.latitude - driver.current_location.latitude
        lon_delta = order.pickup.longitude - driver.current_location.longitude
        return (lat_delta**2 + lon_delta**2) ** 0.5

    selected = min(available, key=distance_score)
    selected.is_available = False
    order.assigned_driver_id = selected.id
    order.status = OrderStatus.DRIVER_ASSIGNED
    return selected
