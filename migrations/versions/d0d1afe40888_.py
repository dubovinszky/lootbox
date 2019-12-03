"""empty message

Revision ID: d0d1afe40888
Revises: 50fb724162e6
Create Date: 2019-11-27 14:19:48.289420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0d1afe40888'
down_revision = '50fb724162e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('log', sa.Column('handed_over', sa.Boolean(), server_default='f', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('log', 'handed_over')
    # ### end Alembic commands ###