from typing import List
from sqlalchemy import String, Integer, Float, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SMWHackInfo(Base):
    __tablename__ = 'smwhacks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    authors: Mapped[List[str]] = mapped_column(String())
    exits: Mapped[int] = mapped_column(Integer())
    difficulty: Mapped[str] = mapped_column(String())
    submissions: Mapped[List[str]] = mapped_column(String())
    earliest_submission: Mapped[float] = mapped_column(Float())
    latest_submission: Mapped[float] = mapped_column(Float())
    acceptances: Mapped[List[str]] = mapped_column(String())
    earliest_acceptance: Mapped[float] = mapped_column(Float(), nullable=True)
    latest_acceptance: Mapped[float] = mapped_column(Float(), nullable=True)
    demo: Mapped[bool] = mapped_column(Integer())
    hall_of_fame: Mapped[bool] = mapped_column(Integer())


class YIHackInfo(Base):
    __tablename__ = 'yihacks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    authors: Mapped[List[str]] = mapped_column(String())
    levels: Mapped[int] = mapped_column(Integer())
    submissions: Mapped[List[str]] = mapped_column(String())
    earliest_submission: Mapped[float] = mapped_column(Float())
    latest_submission: Mapped[float] = mapped_column(Float())
    acceptances: Mapped[List[str]] = mapped_column(String())
    earliest_acceptance: Mapped[float] = mapped_column(Float(), nullable=True)
    latest_acceptance: Mapped[float] = mapped_column(Float(), nullable=True)
    demo: Mapped[bool] = mapped_column(Integer())


class SM64HackInfo(Base):
    __tablename__ = 'sm64hacks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    authors: Mapped[List[str]] = mapped_column(String())
    stars: Mapped[int] = mapped_column(Integer())
    difficulty: Mapped[str] = mapped_column(String())
    submissions: Mapped[List[str]] = mapped_column(String())
    earliest_submission: Mapped[float] = mapped_column(Float())
    latest_submission: Mapped[float] = mapped_column(Float())
    acceptances: Mapped[List[str]] = mapped_column(String())
    earliest_acceptance: Mapped[float] = mapped_column(Float(), nullable=True)
    latest_acceptance: Mapped[float] = mapped_column(Float(), nullable=True)
    demo: Mapped[bool] = mapped_column(Integer())


Games = {
    "SMW": "smwhacks",
    "YI": "yihacks",
    "SM64": "sm64hacks"
}


Tables = {
    "SMW": SMWHackInfo,
    "YI": YIHackInfo,
    "SM64": SM64HackInfo
}
