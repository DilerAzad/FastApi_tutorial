from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate
from .database import Database

app = FastAPI()

db = Database()

### Read a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    return db.get(id)


### Create a new shipment with content and weight
@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> int:
    return db.create(shipment)


### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    return db.update(id, shipment)


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    # Remove from datastore
    return db.delete(id)


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
