"""empty message

Revision ID: b3c08bf4fecc
Revises: c393f60bedb8
Create Date: 2023-01-11 09:56:10.515212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c08bf4fecc'
down_revision = 'c393f60bedb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('data', 'date',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=False)
    op.alter_column('data', 'sumclose',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)
    op.alter_column('data', 'nasclose',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('data', 'nasclose',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('data', 'sumclose',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('data', 'date',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=False)
    # ### end Alembic commands ###
