from enum import Enum
from pydantic import BaseModel, Field


class ShipmentStatus(str, Enum):
    placed = "placed"
    delivered = "delivered"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"

class BaseShipment(BaseModel):
    content: str = Field(max_length=100)
    weight: float = Field(le=25, ge=0)

class ShipmentRead(BaseShipment):
    status: ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus

