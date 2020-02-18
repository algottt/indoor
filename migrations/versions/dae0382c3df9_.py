"""empty message

Revision ID: dae0382c3df9
Revises: e4b8d054ca11
Create Date: 2020-02-18 08:39:40.480336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dae0382c3df9'
down_revision = 'e4b8d054ca11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('comment', sa.String(length=1024), nullable=True),
    sa.Column('src', sa.String(length=256), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_files_comment'), 'files', ['comment'], unique=False)
    op.create_index(op.f('ix_files_created_at'), 'files', ['created_at'], unique=False)
    op.create_index(op.f('ix_files_name'), 'files', ['name'], unique=False)
    op.create_index(op.f('ix_files_updated_at'), 'files', ['updated_at'], unique=False)
    op.alter_column('devices_health', 'device_id',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Integer(),
               existing_nullable=False)
    op.create_foreign_key(None, 'devices_health', 'devices', ['device_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'devices_health', type_='foreignkey')
    op.alter_column('devices_health', 'device_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.drop_index(op.f('ix_files_updated_at'), table_name='files')
    op.drop_index(op.f('ix_files_name'), table_name='files')
    op.drop_index(op.f('ix_files_created_at'), table_name='files')
    op.drop_index(op.f('ix_files_comment'), table_name='files')
    op.drop_table('files')
    # ### end Alembic commands ###
