"""add shipment table

Revision ID: 18b9fa0c2d5e
Revises: 
Create Date: 2026-03-16 16:05:15.245710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18b9fa0c2d5e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "shipment",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("content", sa.CHAR, nullable=False),
        sa.Column("status", sa.CHAR, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("shipment")
