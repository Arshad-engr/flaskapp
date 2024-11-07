"""role identity

Revision ID: 613833bb71ee
Revises: ee7f1fd709e8
Create Date: 2024-10-12 19:46:17.048206

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import uuid


# revision identifiers, used by Alembic.
revision = '613833bb71ee'
down_revision = 'ee7f1fd709e8'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Add the new column without the unique constraint
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fs_uniquifier', sa.String(length=255), nullable=True))
    
    # Step 2: Generate unique values for the fs_uniquifier column for existing records
    user_table = table('user', column('id', sa.Integer), column('fs_uniquifier', sa.String))
    connection = op.get_bind()

    # Assign a unique uuid to each user
    results = connection.execute(sa.select([user_table.c.id])).fetchall()
    for user in results:
        connection.execute(
            user_table.update().where(user_table.c.id == user.id).values(
                fs_uniquifier=str(uuid.uuid4())
            )
        )

    # Step 3: Alter the column to be non-nullable and add the unique constraint
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('fs_uniquifier', existing_type=sa.String(length=255), nullable=False)
        batch_op.create_unique_constraint('uq_user_fs_uniquifier', ['fs_uniquifier'])

def downgrade():
    # Reverse the migration
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_fs_uniquifier', type_='unique')
        batch_op.drop_column('fs_uniquifier')
