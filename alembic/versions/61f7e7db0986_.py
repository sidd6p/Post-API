"""empty message

Revision ID: 61f7e7db0986
Revises: 7919ec999594
Create Date: 2024-02-19 00:58:39.489461

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "61f7e7db0986"
down_revision: Union[str, None] = "7919ec999594"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
