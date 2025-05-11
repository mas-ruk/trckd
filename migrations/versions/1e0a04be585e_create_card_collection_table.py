"""Create card collection table

Revision ID: 1e0a04be585e
Revises: 
Create Date: 2025-05-07 11:49:48.650461
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1e0a04be585e'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create User table
    op.create_table(
        'User',
        sa.Column('user_ID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=50), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('user_ID'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create Card table
    op.create_table(
        'Card',
        sa.Column('card_ID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('type_line', sa.String(length=200), nullable=False),
        sa.Column('colors', sa.String(length=50)),
        sa.Column('rarity', sa.String(length=50)),
        sa.Column('image_uri', sa.String(length=255)),
        sa.Column('user_ID', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_ID'], ['User.user_ID']),
        sa.PrimaryKeyConstraint('card_ID')
    )

def downgrade():
   
    op.drop_table('Card')
    op.drop_table('User')

