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
    type: Mapped[str] = mapped_column(String())
    submissions: Mapped[List[str]] = mapped_column(String())
    earliest_submission: Mapped[float] = mapped_column(Float())
    latest_submission: Mapped[float] = mapped_column(Float())
    acceptances: Mapped[List[str]] = mapped_column(String())
    earliest_acceptance: Mapped[float] = mapped_column(Float(), nullable=True)
    latest_acceptance: Mapped[float] = mapped_column(Float(), nullable=True)
    demo: Mapped[bool] = mapped_column(Integer())
    hall_of_fame: Mapped[bool] = mapped_column(Integer())
    sa_1: Mapped[bool] = mapped_column(Integer())
    collab: Mapped[bool] = mapped_column(Integer())


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
    "Newcomer",
    "Casual",
    "Intermediate",
    "Advanced",
    "Expert",
    "Master",
    "Grandmaster"
]


difficulty_lookup = {
    "newcomer": hack_difficulties[0],
    "casual": hack_difficulties[1],
    "intermediate": hack_difficulties[2],
    "advanced": hack_difficulties[3],
    "expert": hack_difficulties[4],
    "master": hack_difficulties[5],
    "grandmaster": hack_difficulties[6]
}


hack_types = [
    "Standard",
    "Kaizo",
    "Puzzle",
    "Tool-Assisted",
    "Pit"
]


type_lookup = {
    "standard": hack_types[0],
    "kaizo": hack_types[1],
    "puzzle": hack_types[2],
    "tool-assisted": hack_types[3],
    "pit": hack_types[4]
}
