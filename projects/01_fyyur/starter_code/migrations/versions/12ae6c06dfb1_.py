"""empty message

Revision ID: 12ae6c06dfb1
Revises: 14690aa96cf6
Create Date: 2020-05-02 00:04:05.410188

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '12ae6c06dfb1'
down_revision = '14690aa96cf6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show_id',
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'artist_id')
    )
    op.drop_table('show')
    op.alter_column('Artist', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('Venue', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('Artist', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.create_table('show',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], name='show_artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], name='show_venue_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='show_pkey')
    )
    op.drop_table('Show_id')
    # ### end Alembic commands ###
