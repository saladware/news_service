"""comments

Revision ID: d876b69ace76
Revises: 8d8bedae4c19
Create Date: 2023-03-03 17:23:58.532388

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd876b69ace76'
down_revision = '8d8bedae4c19'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('author_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('news_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['news_id'], ['news.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('news', 'author_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('news', 'author_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_table('comments')
    # ### end Alembic commands ###
