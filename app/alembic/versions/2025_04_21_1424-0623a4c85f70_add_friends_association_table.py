"""add friends association table

Revision ID: 0623a4c85f70
Revises: e4dc1b076a76
Create Date: 2025-04-21 14:24:32.627618+03:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0623a4c85f70'
down_revision: Union[str, None] = 'e4dc1b076a76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_friends_association_table',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('friend_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['friend_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'friend_id')
    )
    op.drop_table('user_friends_association_table')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_friends_association_table',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('friend_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['friend_id'], ['users.id'], name='user_friends_association_table_friend_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_friends_association_table_user_id_fkey')
    )
    op.drop_table('users_friends_association_table')
    # ### end Alembic commands ###
