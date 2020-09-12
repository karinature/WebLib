import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, Text, UnicodeText, DateTime, Float, Boolean, PickleType

from sqlalchemy.ext.declarative import declarative_base

from properties import RAW_DATA_DIR

Base = declarative_base()


# class TeamModel(Base):
#     """Data model for teams."""
#     __tablename__ = "sqlalchemy_tutorial_teams"
#     # __table_args__ = {"schema": "example"} #for postgress
#
#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String(100), nullable=False)
#     city = Column(String(100), nullable=False)
#
#     def __repr__(self):
#         return '<Team model {}>'.format(self.id)
#
#
# class PlayerModel(Base):
#     """Data model for players."""
#     __tablename__ = "sqlalchemy_tutorial_players"
#     # __table_args__ = {"schema": "example"} #for postgress
#
#     id = Column(Integer, primary_key=True, nullable=False)
#
#     team_id = Column(Integer, ForeignKey('sqlalchemy_tutorial_teams.id'), nullable=False)  # todo bookmark
#     name = Column(String(100), nullable=False)
#     position = Column(String(100), nullable=False)
#
#     # Relationships #todo bookmark
#     team = relationship("TeamModel", backref="player")
#
#     def __repr__(self):
#         return '<Person model {}>'.format(self.id)


# corresponds to the bookreferences2.csv
class BookRef(Base):
    __tablename__ = 'book_references'

    src_scv = [f'{RAW_DATA_DIR}/{textsfile}'
               for textsfile in os.listdir(RAW_DATA_DIR) if textsfile.startswith('bookreferences')]

    col_names = ['book_biblio_info', 'file', 'titleref', 'gcode']

    dtype_dic_csv2py = {'book bibliographic info': str,  # :int ???
                        'file': str,
                        'titleref': str,
                        'gcode': str}
    dtype_dic_py2sql = {int: Integer, str: Text}

    # todo see if possible to name the fields differently from  their csv name
    #   answer: names of columns here in the model class dont have to be the same as in the original file
    # the fields marked as 'nullable(=True)' are those who doesn't necessarily have a value in the orig (moshes) csv
    dbg_index = Column(Integer, autoincrement=True, primary_key=True, )
    book_biblio_info = Column(String(10), primary_key=True, nullable=False, default='non')
    file = Column(String(100), default='non', nullable=True)
    titleref = Column(String(100), nullable=True)
    gcode = Column(Text, nullable=True)

    # fixme find a better default val or handle empty field. try the option below
    # todo what does it mean to have a column that is both nullable and has a default value
    # file = Column(String(100), default=None, nullable=True) todo try this one

    # gcode = Column(Text, nullable=True ,unique=True)

    def __repr__(self):
        return f'<BookRef model file: {self.file},  title ref: {self.titleref}, index: {self.book_bibliographic_info}>'


# corresponds to the titlesa.csv
class Title(Base):  # todo make sure what each fields
    __tablename__ = 'titles'  # fixme

    src_scv = [f'{RAW_DATA_DIR}/{textsfile}'
               for textsfile in os.listdir(RAW_DATA_DIR) if textsfile.startswith('title')]

    col_names = ['index_org', 'author', 'centend', 'centstart', 'joined', 'language', 'number', 'title']

    dtype_dic_csv2py = {'index1': str,
                        'author1': str,
                        'centend': str,
                        'centstart': str,
                        'joined': str,
                        'language': str,
                        'number': str,
                        'title1': str}
    # dtype_dic_py2sql = {int: Integer, str: Text}

    dbg_index = Column(Integer, autoincrement=True, primary_key=True)
    # the fields marked as 'nullable(=True)' are those who doesn't necessarily have a value in the orig (moshes) csv
    index_org = Column(String(10), primary_key=True, nullable=False, default='non')  # , nullable=False)
    author = Column(String(100))
    centend = Column(String(100))
    centstart = Column(String(100))
    joined = Column(String(200))  # fixme this seems to be alwayws null
    language = Column(String(100))
    number = Column(String(100))
    title = Column(String(500))

    def __repr__(self):
        # todo rename column names
        return f'<Title model title: {self.title},  author: {self.author}, index: {self.index_org}>'


# corresponds to the text_subjects2.csv
class TextSubject(Base):
    # todo fixme
    #  file structure not fully understood
    #  plus what happens when there are miultiple commas
    #   or a subject that contains a comma within brackets(', ")
    __tablename__ = 'text_subjects'  # fixme

    col_names = ['subject', 'C']

    src_scv = [f'{RAW_DATA_DIR}/{textsfile}'
               for textsfile in os.listdir(RAW_DATA_DIR) if textsfile.startswith('texts_subjects')]

    dtype_dic_csv2py = {'subject': str,
                        'C': str}
    dtype_dic_py2sql = {int: Integer, str: Text}

    dbg_index = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(200), nullable=False)
    C = Column(Text)  # longest C value is ~68,000 chars in line 24794/5 &~31268 .. fixme consider creating sub tables

    def __repr__(self):
        return f'<TextSubject subject: {self.subject}, C: {self.C} >'


# corresponds to the textsa1.csv textsa2.csv textsa19.csv textsa1.csv
class TextText(Base):
    __tablename__ = "texts"

    # src_scv = ['/home/fares/PycharmProjects/WebLib/raw_data/textsa1.csv']
    src_scv = ['/home/fares/PycharmProjects/WebLib/raw_data/textsa2.csv']
    # src_scv = ['/home/fares/PycharmProjects/WebLib/raw_data/textsa19.csv']
    # src_scv = [f'{RAW_DATA_DIR}/{textsfile}' fixme should work
    #            for textsfile in os.listdir(RAW_DATA_DIR) if textsfile.startswith('textsa')]

    col_names = ['subject', 'ref', 'page', 'book_biblio_info', 'number', 'C']

    dtype_dic_csv2py = {'subject': str,
                        'ref': str,
                        'page': str,
                        'book bibliographic info': str,  # :int ???
                        'number': str,
                        'C': str}  # {col:str for col in col_names}
    # dtype_dic_py2sql = {int: Integer, str: Text}
    index_dbg = Column(Integer, autoincrement=True, primary_key=True, nullable=False)

    subject = Column(String(120))
    # ref = Column(String(100), nullable=True, server_default='non', default='non')
    ref = Column(String(100))
    page = Column(String(10))
    book_biblio_info = Column(String(10))
    number = Column(String(10))
    C = Column(String(10))

    def __repr__(self):
        return f'<TextText model subject: {self.subject},  C: {self.C}, >'
