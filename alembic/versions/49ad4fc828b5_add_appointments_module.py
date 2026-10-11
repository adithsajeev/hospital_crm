
"""Add appointments module

Revision ID: 49ad4fc828b5
Revises: e15a17969918
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "49ad4fc828b5"
down_revision: Union[str, Sequence[str], None] = "e15a17969918"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add columns only if they don't already exist.
    conn = op.get_bind()
    columns = {
        col["name"]
        for col in sa.inspect(conn).get_columns("appointments")
    }

    if "reason" not in columns:
        op.add_column(
            "appointments",
            sa.Column("reason", sa.Text(), nullable=True),
        )

    if "created_at" not in columns:
        op.add_column(
            "appointments",
            sa.Column("created_at", sa.DateTime(), nullable=True),
        )

    # SQLite needs batch mode for this column alteration.
    with op.batch_alter_table("appointments") as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=sa.VARCHAR(),
            nullable=False,
        )

        # Keep this only if you intentionally want to remove notes.
        batch_op.drop_column("notes")

    # Create the index only if it doesn't already exist.
    indexes = {
        index["name"]
        for index in sa.inspect(op.get_bind()).get_indexes("appointments")
    }
    index_name = op.f("ix_appointments_appointment_date")

    if index_name not in indexes:
        op.create_index(
            index_name,
            "appointments",
            ["appointment_date"],
            unique=False,
        )


def downgrade() -> None:
    # Recreate the previous schema.
    with op.batch_alter_table("appointments") as batch_op:
        batch_op.add_column(
            sa.Column("notes", sa.VARCHAR(), nullable=True)
        )
        batch_op.alter_column(
            "status",
            existing_type=sa.VARCHAR(),
            nullable=True,
        )

    op.drop_index(
        op.f("ix_appointments_appointment_date"),
        table_name="appointments",
    )
    op.drop_column("appointments", "created_at")
    op.drop_column("appointments", "reason")