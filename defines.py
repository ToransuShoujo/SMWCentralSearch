from datetime import datetime
from typing import List
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SMWHackInfo(Base):
    def __repr__(self):
        return f"SMWHackInfo('{self}')"
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
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


hack_difficulties = [
    "Standard: Easy",
    "Standard: Normal",
    "Standard: Hard",
    "Standard: Very Hard",
    "Kaizo: Beginner",
    "Kaizo: Intermediate",
    "Kaizo: Expert",
    "Tool-Assisted: Kaizo",
    "Tool-Assisted: Pit",
    "Misc.: Troll"
]

difficulty_lookup = {
    "standard_easy": hack_difficulties[0],
    "standard_normal": hack_difficulties[1],
    "standard_hard": hack_difficulties[2],
    "standard_very_hard": hack_difficulties[3],
    "kaizo_beginner": hack_difficulties[4],
    "kaizo_intermediate": hack_difficulties[5],
    "kaizo_expert": hack_difficulties[6],
    "tool-assisted_kaizo": hack_difficulties[7],
    "tool-assisted_pit": hack_difficulties[8],
    "misc._troll": hack_difficulties[9]
}
