"""Make full_name nullable

Revision ID: 097b917cc3f3
Revises: b53f680d0719
Create Date: 2025-10-14 08:59:07.508723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '097b917cc3f3'
down_revision: Union[str, None] = 'b53f680d0719'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'full_name',
                    existing_type=sa.String(),
                    nullable=True)


def downgrade() -> None:
    op.alter_column('users', 'full_name',
                    existing_type=sa.String(),
                    nullable=False)
