# Multi-Delivery App Design (Fuel, Groceries, Food, Motocab)

This repository contains a starter architecture and reference implementation for a multi-service logistics app.

## Service lines supported
- Fuel delivery
- Grocery delivery
- Food delivery
- Motocab rides

## High-level architecture
- **Order domain (`app/domain.py`)**: core entities (`CustomerOrder`, `Driver`, `PriceBreakdown`, service enums).
- **Pricing (`app/pricing.py`)**: strategy-based pricing config per service type.
- **Dispatch (`app/dispatcher.py`)**: nearest available driver assignment by service category.
- **API (`app/main.py`)**: FastAPI endpoints for creating and dispatching orders.

## API endpoints
- `GET /health` - service health
- `POST /orders` - create order and return price quote
- `POST /orders/{order_id}/dispatch` - assign driver

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Example order payload
```json
{
  "customer_id": "cust-01",
  "service_type": "food",
  "pickup": {"latitude": 6.49, "longitude": 3.38},
  "dropoff": {"latitude": 6.52, "longitude": 3.42},
  "distance_km": 5.4,
  "items": [
    {"name": "Burger", "quantity": 2, "unit_price": 6.5}
  ]
}
```

## Next design steps
- Add real-time order tracking and event bus (Kafka/RabbitMQ).
- Integrate payment gateway and wallet split settlements per vertical.
- Add role-based apps: customer, merchant/station, rider/driver, admin operations.
- Add geospatial search and ETA modeling with map provider.
- Move from in-memory storage to PostgreSQL + Redis.
