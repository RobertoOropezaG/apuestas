"""6 Add admin to user model

Revision ID: f814138f7d72
Revises: a04b18b2b725
Create Date: 2018-06-24 20:17:39.771781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f814138f7d72'
down_revision = 'a04b18b2b725'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'bet', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'bet', 'bettable', ['bettable_id'], ['id'])
    op.create_foreign_key(None, 'bettable', 'match', ['match_id'], ['id'])
    op.create_foreign_key(None, 'match', 'team', ['team2_id'], ['id'])
    op.create_foreign_key(None, 'match', 'team', ['team1_id'], ['id'])
    op.add_column('user', sa.Column('admin_password', sa.String(200), nullable=True))
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.create_foreign_key(None, 'user', 'identity', ['identity_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'is_admin')
    op.drop_column('user', 'admin_password')
    op.drop_constraint(None, 'match', type_='foreignkey')
    op.drop_constraint(None, 'match', type_='foreignkey')
    op.drop_constraint(None, 'bettable', type_='foreignkey')
    op.drop_constraint(None, 'bet', type_='foreignkey')
    op.drop_constraint(None, 'bet', type_='foreignkey')
    # ### end Alembic commands ###