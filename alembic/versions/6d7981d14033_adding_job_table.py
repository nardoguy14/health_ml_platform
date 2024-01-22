"""adding_job_table

Revision ID: 6d7981d14033
Revises: f3db947925cf
Create Date: 2024-01-21 20:43:33.182190

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = '6d7981d14033'
down_revision: Union[str, None] = 'f3db947925cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data_set_id', sa.Integer, nullable=False),
        sa.Column('model_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DATETIME, nullable=False, server_default=func.now()),
        sa.Column('modified_at', sa.DATETIME, nullable=False, server_default=func.now())
    )


def downgrade() -> None:
    op.drop_table('jobs')
