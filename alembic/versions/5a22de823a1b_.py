"""empty message

Revision ID: 5a22de823a1b
Revises: 61f7e7db0986
Create Date: 2024-02-19 00:59:51.909845

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5a22de823a1b"
down_revision: Union[str, None] = "61f7e7db0986"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("posts", sa.Column("test_new", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts", "test_new")
    # ### end Alembic commands ###