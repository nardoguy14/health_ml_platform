"""adding_new_column_jobs

Revision ID: 86cf2e649cb2
Revises: 68848c974d27
Create Date: 2024-02-01 08:10:54.118243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86cf2e649cb2'
down_revision: Union[str, None] = '68848c974d27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('jobs', sa.Column('job_id', sa.String(length=55)))
    op.add_column('jobs', sa.Column('status', sa.String(length=55)))


def downgrade() -> None:
    op.drop_column('jobs', 'job_id')
    op.drop_column('jobs', 'statusZ')
