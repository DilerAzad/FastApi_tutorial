from sqlalchemy import ARRAY, INTEGER
from docutils.nodes import address
from uuid import UUID, uuid4
import datetime
from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship, Column
from sqlalchemy.dialects import postgresql


class ShipmentStatus(str, Enum):
    placed = "placed"
    delivered = "delivered"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: UUID = Field(sa_column = Column(postgresql.UUID(as_uuid=True), 
    primary_key=True, 
    default=uuid4))

    created_at: datetime.datetime = Field(
        sa_column = Column(postgresql.TIMESTAMP,
        default=datetime.datetime.now())
    )

    content: str = Field(max_length=100)
    weight: float = Field(le=25, ge=0)
    status: ShipmentStatus = Field(default="placed")
    
    estimated_delivery: datetime.datetime = Field(
        default=datetime.datetime.now() + datetime.timedelta(days=3)
    )
    
    seller_id: UUID = Field(foreign_key="seller.id")
    
    seller: "Seller" = Relationship(back_populates="shipments",
    sa_relationship_kwargs={"lazy": "selectin"})

    delivery_partner_id: UUID = Field(foreign_key="delivery_partner.id")
    
    delivery_partner: "DeliveryPartner" = Relationship(back_populates="shipments",
    sa_relationship_kwargs={"lazy": "selectin"})

class User(SQLModel):
    name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)
    password_hash: str  

class Seller(User, table = True):
    __tablename__ = "seller"

    id: UUID = Field(sa_column = Column(postgresql.UUID(as_uuid=True), 
    primary_key=True, 
    default=uuid4))

    created_at: datetime.datetime = Field(
        sa_column = Column(postgresql.TIMESTAMP,
        default=datetime.datetime.now())
    )


    name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)
    password_hash: str
    address: int | None = None

    shipments: list[Shipment] = Relationship(back_populates="seller",
    sa_relationship_kwargs={"lazy": "selectin"})

class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"

    id: UUID = Field(
        sa_column = Column(postgresql.UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4)
    )

    created_at: datetime.datetime = Field(
        sa_column = Column(postgresql.TIMESTAMP,
        default=datetime.datetime.now())
    )

    serviceable_zip_codes: list[int] = Field(
        sa_column = Column(ARRAY(INTEGER)),
        )
    
    max_handling_capacity: int

    shipments: list[Shipment] = Relationship(back_populates="delivery_partner",
    sa_relationship_kwargs={"lazy": "selectin"})