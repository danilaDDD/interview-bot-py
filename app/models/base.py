from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.setting.setting import now_with_tz


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=now_with_tz, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=now_with_tz, onupdate=now_with_tz, nullable=False)


class AbsId(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)