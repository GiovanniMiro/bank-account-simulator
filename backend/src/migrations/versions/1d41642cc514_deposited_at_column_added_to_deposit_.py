"""deposited_at column added to deposit table

Revision ID: 1d41642cc514
Revises: bc18cbd86c8e
Create Date: 2025-01-30 22:01:24.277625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d41642cc514'
down_revision = 'bc18cbd86c8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('deposits', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deposited_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('deposits', schema=None) as batch_op:
        batch_op.drop_column('deposited_at')

    # ### end Alembic commands ###
