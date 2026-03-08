from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.database.models import Shipment
from app.database.session import SessionDep, create_db_tables

from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(lifespan=lifespan_handler)


### Read a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
    shipment = session.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipment


### Create a new shipment with content and weight
@app.post("/shipment", response_model=dict[str, int])
def submit_shipment(shipment: ShipmentCreate, session: SessionDep):
    new_shipment = Shipment(**shipment.model_dump())
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


### Update an existing shipment
@app.patch("/shipment", response_model=ShipmentUpdate)
def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    update = shipment_update.model_dump(exclude_none=True)

    if update is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )
    shipment = session.get(Shipment, id)
    shipment.sqlmodel_update(update)  # ty:ignore[possibly-missing-attribute]

    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


### Delete a Shipment
@app.delete("/shipment", response_model=dict[str, str])
def delete_shipment(id: int, session: SessionDep):
    session.delete(session.get(Shipment, id))
    session.commit()

    return {"detail": f"Shipment with id #{id} is deleted!"}


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
