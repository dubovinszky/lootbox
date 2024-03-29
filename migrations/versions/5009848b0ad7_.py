"""empty message

Revision ID: 5009848b0ad7
Revises: 21dc93c1462f
Create Date: 2019-11-29 13:40:21.662215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5009848b0ad7'
down_revision = '21dc93c1462f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', sa.Boolean(), server_default='t', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'active')
    # ### end Alembic commands ###
