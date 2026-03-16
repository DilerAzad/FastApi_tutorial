from uuid import UUID
from app.api.dependencies import SellerDep
from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import ShipmentServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

router = APIRouter(prefix="/shipment", tags = ["Shipment"])

### Read a shipment by id
@router.get("/", response_model=ShipmentRead)
async def get_shipment(id: UUID, service: ShipmentServiceDep):
    shipment = await service.get(id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipment


### Create a new shipment with content and weight
@router.post("/", response_model=dict[str, UUID])
async def submit_shipment(
    shipment: ShipmentCreate, 
    seller: SellerDep,
    service: ShipmentServiceDep
    ):
    new_shipment = await service.add(shipment, seller)

    return {"id": new_shipment.id}


### Update an existing shipment
@router.patch("/", response_model=ShipmentUpdate)
async def update_shipment(id: UUID, shipment_update: ShipmentUpdate, service: ShipmentServiceDep):
    update = shipment_update.model_dump(exclude_none=True)

    if update is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )
    shipment = await service.update(id, update)
    return shipment


### Delete a Shipment
@router.delete("/", response_model=dict[str, str])
async def delete_shipment(id: UUID, service: ShipmentServiceDep):
    await service.delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}

