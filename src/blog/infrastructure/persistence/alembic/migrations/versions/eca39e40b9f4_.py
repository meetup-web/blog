"""empty message

Revision ID: eca39e40b9f4
Revises:
Create Date: 2025-03-17 20:44:20.817664

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "eca39e40b9f4"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "outbox",
        sa.Column("message_id", sa.UUID(), nullable=False),
        sa.Column("data", sa.Text(), nullable=False),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("message_id"),
    )
    op.create_table(
        "posts",
        sa.Column("post_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("creator_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("post_id"),
    )
    op.create_table(
        "comments",
        sa.Column("comment_id", sa.UUID(), nullable=False),
        sa.Column("post_id", sa.UUID(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("creator_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["posts.post_id"]),
        sa.PrimaryKeyConstraint("comment_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("comments")
    op.drop_table("posts")
    op.drop_table("outbox")
    # ### end Alembic commands ###
