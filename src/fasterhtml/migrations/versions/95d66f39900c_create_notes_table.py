"""Create notes table

Revision ID: 95d66f39900c
Revises: 
Create Date: 2024-08-05 20:55:57.855139

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "95d66f39900c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notes",
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("text", sqlalchemy.String),
        sqlalchemy.Column("completed", sqlalchemy.Boolean),
    )


def downgrade() -> None:
    pass
