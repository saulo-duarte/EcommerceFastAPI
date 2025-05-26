"""add intermediate table to coupons

Revision ID: 9fa227c5bde8
Revises: 097e5e18f37d
Create Date: 2025-05-26 10:15:01.257870

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '9fa227c5bde8'
down_revision: Union[str, None] = '097e5e18f37d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
