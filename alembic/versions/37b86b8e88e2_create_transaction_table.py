"""create transaction table

Revision ID: 37b86b8e88e2
Revises: c1fb78378188
Create Date: 2023-03-17 14:55:10.972285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37b86b8e88e2'
down_revision = 'c1fb78378188'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('value', sa.Numeric(), nullable=False,server_default=sa.text('0')),
        sa.Column('name_movement',sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('user_id', sa.Integer, nullable=False)
        )
    op.create_foreign_key('transactions_user_fk', source_table='transactions', referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass

def downgrade() -> None:
    op.drop_table('transactions')
    #op.drop_constraint('transactions_user_fk',table_name='transactions')
    
    pass
