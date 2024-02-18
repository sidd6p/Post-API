"""empty message

Revision ID: 7919ec999594
Revises: 0816ef994432
Create Date: 2024-02-19 00:57:20.424459

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7919ec999594"
down_revision: Union[str, None] = "0816ef994432"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
