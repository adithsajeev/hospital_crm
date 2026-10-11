
"""add user relationship to doctors

Revision ID: 87a9f6d93908
Revises: 3c6cf0ac91a5
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "87a9f6d93908"
down_revision: Union[str, Sequence[str], None] = "3c6cf0ac91a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("doctors", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column("user_id", sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            "fk_doctors_user_id_users",
            "users",
            ["user_id"],
            ["id"],
        )
        batch_op.create_unique_constraint(
            "uq_doctors_user_id",
            ["user_id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("doctors", recreate="always") as batch_op:
        batch_op.drop_constraint(
            "uq_doctors_user_id",
            type_="unique",
        )
        batch_op.drop_constraint(
            "fk_doctors_user_id_users",
            type_="foreignkey",
        )
        batch_op.drop_column("user_id")