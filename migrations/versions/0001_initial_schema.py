"""Initial schema: sessions and responses, with understanding and usefulness ratings.

Revision ID: 0001
Revises:
Create Date: 2026-11-23

Generated with `flask --app app db migrate` from models.py, then renamed.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('sessions',
    sa.Column('session_id', sa.String(length=36), nullable=False),
    sa.Column('scenario_id', sa.String(length=20), nullable=False),
    sa.Column('content_version', sa.String(length=120), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('pre_understanding', sa.Integer(), nullable=True),
    sa.Column('post_understanding', sa.Integer(), nullable=True),
    sa.Column('usefulness', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('session_id')
    )
    op.create_table('responses',
    sa.Column('response_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.String(length=36), nullable=False),
    sa.Column('decision_point_id', sa.String(length=20), nullable=False),
    sa.Column('option_id', sa.String(length=5), nullable=False),
    sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.session_id'], ),
    sa.PrimaryKeyConstraint('response_id'),
    sa.UniqueConstraint('session_id', 'decision_point_id', name='one_answer_per_decision')
    )
    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_responses_session_id'), ['session_id'], unique=False)


def downgrade():
    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_responses_session_id'))

    op.drop_table('responses')
    op.drop_table('sessions')
    