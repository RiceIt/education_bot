import datetime

from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Countries(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True)
    name = Column(String)


class Institutes(Base):
    __tablename__ = "institutes"

    institute_id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(Integer, ForeignKey("countries.country_id"), nullable=True)


class Departments(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True)
    name = Column(String)
    institute = Column(Integer, ForeignKey("institutes.institute_id"), nullable=True)


subjects_disciplines_table = Table(
    'subjects_disciplines_table', Base.metadata,
    Column('subject_id', Integer, ForeignKey('subjects.subject_id')),
    Column('discipline_id', Integer, ForeignKey('disciplines.discipline_id')),
)


class Disciplines(Base):
    __tablename__ = "disciplines"

    discipline_id = Column(Integer, primary_key=True)
    name = Column(String)
    platform_id = Column(Integer, ForeignKey('platforms.platform_id'))


subjects_programs_table = Table(
    'subjects_programs_table', Base.metadata,
    Column('subject_id', Integer, ForeignKey('subjects.subject_id')),
    Column('program_id', Integer, ForeignKey('programs.program_id'))
)


class Subjects(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True)
    name = Column(String)
    discipline = relationship("Disciplines",
                              secondary=subjects_disciplines_table,
                              backref="subjects")
    programs = relationship("Programs",
                            secondary=subjects_programs_table,
                            backref="subjects")


class Programs(Base):
    __tablename__ = "programs"

    program_id = Column(Integer, primary_key=True)
    program_id_in_platform = Column(String)
    platform = Column(String)
    title = Column(String)
    url = Column(String)
    department = Column(Integer, ForeignKey("departments.department_id"))
    type = Column(String)
    funded = Column(String)

    __table_args__ = (
        UniqueConstraint('program_id_in_platform', 'platform', name='_program_unique_id'),
    )


disciplines_users_table = Table(
    'disciplines_users_table', Base.metadata,
    Column('discipline_id', Integer, ForeignKey('disciplines.discipline_id')),
    Column('user_id', Integer, ForeignKey('users.user_id'))
)

countries_users_table = Table(
    'countries_users_table', Base.metadata,
    Column('country_id', Integer, ForeignKey('countries.country_id')),
    Column('user_id', Integer, ForeignKey('users.user_id'))
)

institutes_users_table = Table(
    'institutes_users_table', Base.metadata,
    Column('institute_id', Integer, ForeignKey('institutes.institute_id')),
    Column('user_id', Integer, ForeignKey('users.user_id'))
)


class Platform(Base):
    __tablename__ = "platforms"

    platform_id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)


degrees_users_table = Table(
    'degrees_users_table', Base.metadata,
    Column('degree_id', Integer, ForeignKey('degrees.degree_id')),
    Column('user_id', Integer, ForeignKey('users.user_id'))
)


class Degree(Base):
    __tablename__ = "degrees"

    degree_id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    psw = Column(String(255), unique=True)
    is_active = Column(Boolean)
    silent_mode = Column(Boolean)
    adding_filters = Column(Boolean)
    current_platform = Column(String(255))
    date = Column(DateTime, default=datetime.datetime.utcnow())
    discipline = relationship("Disciplines",
                              secondary=disciplines_users_table,
                              backref="users")
    country = relationship("Countries",
                           secondary=countries_users_table,
                           backref="users")
    institutes = relationship("Institutes",
                              secondary=institutes_users_table,
                              backref="users")
    degrees = relationship("Degree",
                           secondary=degrees_users_table,
                           backref="users")
    type = Column(String)
    funded = Column(String)

    def __repr__(self):
        return f"User {self.chat_id}"
