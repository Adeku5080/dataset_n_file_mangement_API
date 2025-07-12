"""Add search_vector column and GIN index

Revision ID: 3c3d3630659b
Revises: eaa8efdeb622
Create Date: 2025-07-12 10:37:20.017688
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '3c3d3630659b'
down_revision = 'eaa8efdeb622'
branch_labels = None
depends_on = None

def upgrade():
    # Add the search_vector column to datasets
    op.add_column('datasets', sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True))
    
    # Create a GIN index on search_vector
    op.create_index(
        'ix_datasets_search_vector',
        'datasets',
        ['search_vector'],
        postgresql_using='gin'
    )

def downgrade():
    # Drop the GIN index and search_vector column
    op.drop_index('ix_datasets_search_vector', table_name='datasets')
    op.drop_column('datasets', 'search_vector')
