from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from app.domain import CustomerOrder, PriceBreakdown, ServiceType


@dataclass
class PricingConfig:
    base_fee: float
    per_km_fee: float
    service_pct: float


class PricingEngine:
    """Strategy-based pricing engine for multiple delivery verticals."""

    def __init__(self) -> None:
        self._configs: Dict[ServiceType, PricingConfig] = {
            ServiceType.FUEL: PricingConfig(base_fee=1.5, per_km_fee=0.45, service_pct=0.05),
            ServiceType.GROCERIES: PricingConfig(base_fee=2.0, per_km_fee=0.55, service_pct=0.08),
            ServiceType.FOOD: PricingConfig(base_fee=1.8, per_km_fee=0.65, service_pct=0.1),
            ServiceType.MOTOCAB: PricingConfig(base_fee=1.0, per_km_fee=0.75, service_pct=0.0),
        }

    def quote(self, order: CustomerOrder, demand_index: float = 1.0) -> PriceBreakdown:
        config = self._configs[order.service_type]
        distance_fee = round(order.distance_km * config.per_km_fee, 2)
        service_fee = round(order.basket_total * config.service_pct, 2)
        return PriceBreakdown(
            base_fee=config.base_fee,
            distance_fee=distance_fee,
            service_fee=service_fee,
            surge_multiplier=max(1.0, demand_index),
        )
