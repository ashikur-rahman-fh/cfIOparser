"""create settings table

Revision ID: 8351fa78488b
Revises: 
Create Date: 2023-07-08 14:53:20.237986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8351fa78488b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'settings',
        sa.Column('key', sa.String(50), primary_key=True),
        sa.Column('default', sa.String(500)),
        sa.Column('custom', sa.String(500)),
    )


def downgrade() -> None:
    op.drop_table('settings')
