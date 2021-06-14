from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from parser.config import Configuration
from db.schema import Disciplines, Countries, Institutes, Programs, Users, disciplines_users_table, Degree
from dev.dump_disciplines_to_db import parse_subject_list
from parser.funcs import get_keyboard_button
from parser.platforms import AbstractPlatform


engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(engine, future=True)

INPUT_DATA = (
    ("Arts", "https://www.findaphd.com/phds/arts/?10g010&Show=M"),
    ("Biological & Medical Sciences", "https://www.findaphd.com/phds/biological-and-medical-sciences/?10gc00&Show=M"),
    ("Business & Finance", "https://www.findaphd.com/phds/business-and-finance/?10gU00&Show=M"),
    ("Chemical Sciences", "https://www.findaphd.com/phds/chemical-sciences/?10gg00&Show=M"),
    ("Earth Sciences", "https://www.findaphd.com/phds/earth-sciences/?10go00&Show=M"),
    ("Education", "https://www.findaphd.com/phds/education/?10g410&Show=M"),
    ("Engineering", "https://www.findaphd.com/phds/engineering/?10gs00&Show=M"),
    ("Humanities", "https://www.findaphd.com/phds/humanities/?10gE00&Show=M"),
    ("Law", "https://www.findaphd.com/phds/law/?10gY00&Show=M"),
    ("Maths & Computing", "https://www.findaphd.com/phds/maths-and-computing/?10gw00&Show=M"),
    ("Physical Sciences", "https://www.findaphd.com/phds/physical-sciences/?10gk00&Show=M"),
    ("Social Science", "https://www.findaphd.com/phds/social-science-and-health/?10gQ00&Show=M"),
)


def parse_disciplines_and_add_to_db():
    for name, url in INPUT_DATA:
        with Session() as session:
            discipline = Disciplines(name=name)
            session.add(discipline)
            session.commit()
            subject_list = parse_subject_list(discipline.discipline_id, url)
            session.add_all(subject_list)
            session.commit()


def select_program(program_id):
    with Session() as session:
        query = select(Programs).filter_by(program_id=program_id)
        program = session.execute(query).first()
        return program


def insert_program(program: AbstractPlatform):
    pass


def send_notifications(program: AbstractPlatform):
    pass


def add_user(chat_id):
    with Session() as session:
        try:
            user = Users(chat_id=chat_id)
            session.add(user)
            session.commit()
        except IntegrityError:
            pass


def select_discipline_names_buttons(chat_id):
    with Session() as session:
        user = session.query(Users).filter_by(chat_id=chat_id).first()
        disciplines = session.query(Disciplines).all()
        user_disciplines = session.query(Disciplines).filter(Disciplines.users.contains(user)).all()
        disciplines_names = map(lambda d: (f"✅ {d.name}", f"{d.name}:{d.platform_id}") if d in user_disciplines else (d.name, f"{d.name}:{d.platform_id}"), disciplines)
        disciplines_names_buttons = [{"text": text, "callback_data": f"Disciplines:{callback_data}"} for text, callback_data in disciplines_names]
        disciplines_names_buttons = get_keyboard_button(disciplines_names_buttons)
        return disciplines_names_buttons


def select_country_names_buttons(chat_id):
    with Session() as session:
        user = session.query(Users).filter_by(chat_id=chat_id).first()
        countries = session.query(Countries).all()
        user_countries = session.query(Countries).filter(Countries.users.contains(user)).all()
        countries_names = map(lambda c: (f"✅ {c.name}", c.name) if c in user_countries else (c.name, c.name), countries)
        countries_names_buttons = [{"text": text, "callback_data": f"Countries:{callback_data}"} for text, callback_data in countries_names]
        countries_names_buttons = get_keyboard_button(countries_names_buttons)
        return countries_names_buttons


def select_degree_names_buttons(chat_id):
    with Session() as session:
        user = session.query(Users).filter_by(chat_id=chat_id).first()
        countries = session.query(Degree).all()
        user_countries = session.query(Degree).filter(Degree.users.contains(user)).all()
        degrees_names = map(lambda d: (f"✅ {d.name}", d.name) if d in user_countries else (d.name, d.name), countries)
        degrees_names_buttons = [{"text": text, "callback_data": f"Degrees:{callback_data}"} for text, callback_data in degrees_names]
        degrees_names_buttons = get_keyboard_button(degrees_names_buttons)
        return degrees_names_buttons

# FIXME
# def select_institute_names_buttons(chat_id, limit, offset):
#     with Session() as session:
#         user = session.query(Users).filter_by(chat_id=chat_id).first()
#         institutes = session.query(Institutes).offset(offset).limit(limit).all()
#         institute_names = sorted([i.name for i in institutes])
#         print(len(institute_names))
#
#         user_institutes = session.query(Institutes).filter(Institutes.users.contains(user)).offset(offset).limit(limit).all()
#         checked_institutes = [user_institute.name for user_institute in user_institutes]
#         print(len(checked_institutes))
#         unchecked_institutes = list(set(institute_names) - set(checked_institutes))
#         print(len(unchecked_institutes))
#         checked_institutes = [institute + " ✅" for institute in checked_institutes]
#         result = [[{"text": d, "callback_data": f"Institutes:{institute_names[i]}"}, ] for i, d in enumerate(sorted(unchecked_institutes + checked_institutes))]
#         print(len(result))
#         return result


def create_or_delete_discipline(chat_id, discipline_name, platform):
    with Session() as session:
        print(discipline_name)
        user = session.query(Users).filter_by(chat_id=chat_id).first()
        user_disciplines = user.discipline
        discipline = session.query(Disciplines).filter_by(name=discipline_name, platform_id=platform).first()
        if discipline in user_disciplines:
            user.discipline.remove(discipline)
        else:
            user.discipline.append(discipline)

        session.commit()


def create_or_delete_country(chat_id, country_name):
    with Session() as session:
        user = session.query(Users).filter_by(chat_id=chat_id).first()
        user_countries = user.country
        country = session.query(Countries).filter_by(name=country_name).first()

        if country in user_countries:
            user.country.remove(country)
        else:
            user.country.append(country)

        session.commit()


def create_or_delete_degree(chat_id, degree_name):
    with Session() as session:
        user = session.query(Users).filter_by(chat_id=chat_id).first()
        user_degrees = user.degrees
        degree = session.query(Degree).filter_by(name=degree_name).first()

        if degree in user_degrees:
            user.degrees.remove(degree)
        else:
            user.degrees.append(degree)

        session.commit()


# def create_or_delete_institute(chat_id, institute_name):
#     with Session() as session:
#         user = session.query(Users).filter_by(chat_id=chat_id).first()
#         user_institutes = user.institute
#         institute = session.query(Institutes).filter_by(name=institute_name).first()
#
#         if institute in user_institutes:
#             user.institute.remove(institute)
#         else:
#             user.institute.append(institute)
#
#         session.commit()
