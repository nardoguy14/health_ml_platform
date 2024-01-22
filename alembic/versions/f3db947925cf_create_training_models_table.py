"""create_training_models_table

Revision ID: f3db947925cf
Revises: 
Create Date: 2024-01-18 22:53:27.729287

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import datetime
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = 'f3db947925cf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'training_models',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=40), nullable=False),
        sa.Column('training_data_location', sa.String(length=255), nullable=False),
        sa.Column('t_dep_column', sa.String(length=50), nullable=False),
        sa.Column('layers', sa.JSON, nullable=False),
        sa.Column('created_at', sa.DATETIME, nullable=False, server_default=func.now()),
        sa.Column('modified_at', sa.DATETIME, nullable=False, server_default=func.now())
    )


def downgrade() -> None:
    op.drop_table('training_models')
