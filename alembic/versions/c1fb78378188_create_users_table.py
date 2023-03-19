"""create users table

Revision ID: c1fb78378188
Revises: 
Create Date: 2023-03-16 21:38:25.964668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1fb78378188'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('balance', sa.Numeric(), nullable=False, server_default=sa.text('0')),
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
