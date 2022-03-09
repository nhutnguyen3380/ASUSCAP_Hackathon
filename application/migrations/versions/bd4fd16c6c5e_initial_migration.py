"""Initial Migration

Revision ID: bd4fd16c6c5e
Revises: 
Create Date: 2022-03-08 20:29:53.895291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd4fd16c6c5e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'item', 'order', ['order_id'], ['id'])
    op.add_column('order', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_column('order', 'order_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('order_id', sa.INTEGER(), nullable=False))
    op.drop_column('order', 'id')
    op.drop_constraint(None, 'item', type_='foreignkey')
    # ### end Alembic commands ###
