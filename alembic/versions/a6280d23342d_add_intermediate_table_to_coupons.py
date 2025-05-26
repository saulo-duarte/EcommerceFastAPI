"""add intermediate table to coupons

Revision ID: a6280d23342d
Revises: 9fa227c5bde8
Create Date: 2025-05-26 10:16:22.603407

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'a6280d23342d'
down_revision: Union[str, None] = '9fa227c5bde8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
