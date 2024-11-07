"""Add user_profile field to User model

Revision ID: ff66d9fae575
Revises: bc4937f9a94a
Create Date: 2024-10-10 14:33:53.958796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff66d9fae575'
down_revision = 'bc4937f9a94a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profil_image', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('profil_image')

    # ### end Alembic commands ###