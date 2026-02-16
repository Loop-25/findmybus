from __future__ import annotations

from typing import Dict, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.dispatcher import assign_driver
from app.domain import CustomerOrder, DeliveryItem, Driver, Location, OrderStatus, ServiceType
from app.pricing import PricingEngine

app = FastAPI(title="Multi-Delivery Platform API")
pricing_engine = PricingEngine()

ORDERS: Dict[str, CustomerOrder] = {}
DRIVERS: List[Driver] = [
    Driver(id="drv-fuel-1", service_type=ServiceType.FUEL, current_location=Location(6.55, 3.36)),
    Driver(id="drv-grocery-1", service_type=ServiceType.GROCERIES, current_location=Location(6.47, 3.39)),
    Driver(id="drv-food-1", service_type=ServiceType.FOOD, current_location=Location(6.50, 3.33)),
    Driver(id="drv-motocab-1", service_type=ServiceType.MOTOCAB, current_location=Location(6.51, 3.31)),
]


class LocationIn(BaseModel):
    latitude: float
    longitude: float


class ItemIn(BaseModel):
    name: str
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)


class CreateOrderIn(BaseModel):
    customer_id: str
    service_type: ServiceType
    pickup: LocationIn
    dropoff: LocationIn
    distance_km: float = Field(gt=0)
    items: List[ItemIn] = Field(default_factory=list)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/orders")
def create_order(payload: CreateOrderIn) -> dict:
    order_id = str(uuid4())
    order = CustomerOrder(
        id=order_id,
        customer_id=payload.customer_id,
        service_type=payload.service_type,
        pickup=Location(**payload.pickup.model_dump()),
        dropoff=Location(**payload.dropoff.model_dump()),
        distance_km=payload.distance_km,
        items=[DeliveryItem(**item.model_dump()) for item in payload.items],
    )

    quote = pricing_engine.quote(order, demand_index=1.2)
    order.status = OrderStatus.PRICED
    ORDERS[order_id] = order

    return {
        "order_id": order_id,
        "service_type": order.service_type,
        "price": quote.total,
        "price_breakdown": quote.__dict__,
        "status": order.status,
    }


@app.post("/orders/{order_id}/dispatch")
def dispatch_order(order_id: str) -> dict:
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    driver = assign_driver(order, DRIVERS)
    if not driver:
        raise HTTPException(status_code=409, detail="No available driver for service")

    return {
        "order_id": order.id,
        "driver_id": driver.id,
        "service_type": order.service_type,
        "status": order.status,
    }
