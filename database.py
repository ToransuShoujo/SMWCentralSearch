from sqlalchemy import create_engine, select, text, column, or_
from sqlalchemy.orm import Session
import datetime_management
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


def search_hack(search_dict, game="SMW"):
    table = defines.Tables[game]
    query = select(table)
    difficulties = []
    results_list = []

    for key in search_dict.keys():
        value = search_dict.get(key)
        if key == 'txt-title':
            title_query = value
            # Default is False, so we test for True
            if search_dict.get('bool-title-regex') is not None:
                query = query.where(table.title.regexp_match(title_query))
                continue
            # Default is True, so we test for False.
            elif search_dict.get('bool-title-exact_match') is not None:
                title_query = f'%{title_query}%'
            query = query.where(table.title.like(title_query))
        elif key == 'txt-authors':
            authors_query = value
            # Default is False, so we test for True
            if search_dict.get('bool-authors-regex') is not None:
                query = query.where(table.authors.regexp_match(authors_query))
                continue
            if ', ' in authors_query:
                authors_query = authors_query.replace(', ', ',')
            authors_query = authors_query.split(',')
            for i in range(0, len(authors_query)):
                author = f'%{authors_query[i]}%'
                authors_query.pop(i)
                authors_query.insert(i, author)
            for author in authors_query:
                query = query.where(table.authors.like(author))
        elif key.startswith('listbox'):
            difficulty = key[8:]
            difficulties.append(difficulty)
        elif key == 'txt-exits':
            exit_operator = value[0]
            if exit_operator == '>':
                query = query.where(table.exits > int(value[1:]))
            elif exit_operator == '<':
                query = query.where(table.exits < int(value[1:]))
            elif not exit_operator.isnumeric():
                query = query.where(table.exits == int(value[1:]))
            else:
                query = query.where(table.exits == int(value))
        elif key == 'bool-demo':
            query = query.where(table.demo == 1)
        elif key == 'bool-hall_of_fame':
            query = query.where(table.hall_of_fame == 1)
        elif key.startswith('date'):
            date_property = key.split('-')[1]
            time = search_dict.get(f'txt-time-{date_property}')
            search_type = search_dict.get(f'radio-time-{date_property}')
            datetime = datetime_management.dict_to_datetime(value, time)
            timestamp = datetime_management.convert_to_timestamp(datetime, "datetime")
            if date_property == 'before':
                # Default is Accepted, so we test for Submitted
                if search_type is not None:
                    query = query.filter(table.earliest_submission < timestamp)
                else:
                    query = query.filter(table.earliest_acceptance < timestamp)
            else:
                if search_type is not None:
                    query = query.filter(table.earliest_submission > timestamp)
                else:
                    query = query.filter(table.earliest_acceptance > timestamp)
    if len(difficulties) > 0:
        for difficulty in difficulties:
            difficulty = f'%{defines.difficulty_lookup[difficulty]}%'
            query = query.where(table.difficulty.like(difficulty))
    print(str(query))
    with Session(engine) as session:
        for row in session.execute(query).all():
            results_list.append(row._mapping.get('SMWHackInfo'))
        return results_list
