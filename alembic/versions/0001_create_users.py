"""create users

Revision ID: 0001_create_users
Revises: 
Create Date: 2026-03-17
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_create_users"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(sa.Sequence("entity_id_seq", start=100000, increment=1)))
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), server_default=sa.text("nextval('entity_id_seq')"), nullable=False),
        sa.Column("tg_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_tg_id"), "users", ["tg_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_tg_id"), table_name="users")
    op.drop_table("users")
    op.execute(sa.schema.DropSequence(sa.Sequence("entity_id_seq")))
