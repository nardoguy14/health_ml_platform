"""create_dataset_table

Revision ID: 68848c974d27
Revises: 6d7981d14033
Create Date: 2024-01-21 20:59:41.182875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func


# revision identifiers, used by Alembic.
revision: str = '68848c974d27'
down_revision: Union[str, None] = '6d7981d14033'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'data_set',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('s3_location', sa.String, nullable=False),
        sa.Column('file_name', sa.String, nullable=False),
        sa.Column('created_at', sa.DATETIME, nullable=False, server_default=func.now()),
        sa.Column('modified_at', sa.DATETIME, nullable=False, server_default=func.now())
    )


def downgrade() -> None:
    op.drop_table("data_set")
