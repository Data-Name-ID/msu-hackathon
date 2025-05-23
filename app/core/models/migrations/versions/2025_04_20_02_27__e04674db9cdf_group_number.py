# group number

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "e04674db9cdf"
down_revision: str | None = "5354a2a1ed69"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("groups", sa.Column("number", sa.String(length=10), nullable=False))
    op.create_unique_constraint(op.f("uq_groups_number"), "groups", ["number"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq_groups_number"), "groups", type_="unique")
    op.drop_column("groups", "number")
    # ### end Alembic commands ###
