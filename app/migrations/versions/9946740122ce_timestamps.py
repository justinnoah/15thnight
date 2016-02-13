"""timestamps

Revision ID: 9946740122ce
Revises: c65334ef795d
Create Date: 2016-02-13 12:07:49.690451

"""

# revision identifiers, used by Alembic.
revision = '9946740122ce'
down_revision = 'c65334ef795d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alerts', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updated', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated')
    op.drop_column('users', 'created_at')
    op.drop_column('alerts', 'created_at')
    ### end Alembic commands ###