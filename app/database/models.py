import datetime
from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class ShipmentStatus(str, Enum):
    placed = "placed"
    delivered = "delivered"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: int = Field(primary_key=True, default=None)
    content: str = Field(max_length=100)
    weight: float = Field(le=25, ge=0)
    status: ShipmentStatus = Field(default="placed")
    estimated_delivery: datetime.datetime = Field(
        default=datetime.datetime.now() + datetime.timedelta(days=3)
    )

class Seller(SQLModel, table = True):
    __tablename__ = "seller"

    id: int = Field(primary_key=True, default=None)
    name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)
    password_hash: str