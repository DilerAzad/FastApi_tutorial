import datetime

from pydantic import BaseModel, Field

from app.database.models import ShipmentStatus


class BaseShipment(BaseModel):
    content: str = Field(max_length=100)
    weight: float = Field(le=25, ge=0)


class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime.datetime


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime.datetime | None = Field(default=None)
