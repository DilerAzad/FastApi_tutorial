"""add destination column

Revision ID: abfa4d5aa8a7
Revises: 18b9fa0c2d5e
Create Date: 2026-03-16 16:44:13.177212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abfa4d5aa8a7'
down_revision: Union[str, Sequence[str], None] = '18b9fa0c2d5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "shipment",
        sa.Column("destination", sa.INTEGER, nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("shipment", "destination")
