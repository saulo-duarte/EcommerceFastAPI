"""change user address to be one to many

Revision ID: 4702beca2790
Revises: f6bc197c84dc
Create Date: 2025-05-22 19:34:43.339455

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '4702beca2790'
down_revision: Union[str, None] = 'f6bc197c84dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
