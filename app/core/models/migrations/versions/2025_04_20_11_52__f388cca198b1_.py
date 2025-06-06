
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f388cca198b1"
down_revision: str | None = "a37913975f52"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("tasks", "description", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("tasks", "description", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###
