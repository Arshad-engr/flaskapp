"""Add is_active field to User model

Revision ID: bc4937f9a94a
Revises: 
Create Date: 2024-10-08 12:50:21.594445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc4937f9a94a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add column with server_default=True for existing rows
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()))

    # Remove the server_default if not needed for future rows (optional)
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('is_active', server_default=None)


def downgrade():
    # Remove the is_active column
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')
