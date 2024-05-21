from sqlalchemy import create_engine, select, text, column
from sqlalchemy.orm import Session
import defines

engine = create_engine('sqlite:///smw_central.db', echo=True)
defines.Base.metadata.create_all(engine)


def insert_smw_hacks(hacks):
    if type(hacks) is list and len(hacks) > 0:
        for hack in hacks:
            hacks_to_insert = []
            with Session(engine) as session:
                hack_object = defines.SMWHackInfo(
                    id=hack.id,
                    title=hack.title,
                    authors=hack.authors,
                    exits=hack.exits,
                    difficulty=hack.difficulty,
                    submissions=hack.submissions,
                    earliest_submission=hack.earliest_submission,
                    latest_submission=hack.latest_submission,
                    acceptances=hack.acceptances,
                    earliest_acceptance=hack.earliest_acceptance,
                    latest_acceptance=hack.latest_acceptance,
                    demo=hack.demo,
                    hall_of_fame=hack.hall_of_fame
                )
                hacks_to_insert.append(hack_object)
            session.add_all(hacks_to_insert)
            session.commit()


def get_most_recent_hack(game="SMW"):
    table = defines.Tables[game]
    query = select(table.id).order_by(table.id.desc())
    with Session(engine) as session:
        row = session.execute(query).first()
        if row is None:
            return 0
        else:
            return row[0]


def get_hack(hack_id, game="SMW"):
    table = defines.Tables[game]
    query = select(table).where(table.id == int(hack_id))
    with Session(engine) as session:
        row = session.execute(query).first()
        if row is None:
            return None
        else:
            return row[0]