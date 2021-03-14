from sqlalchemy import ForeignKey, create_engine, MetaData, Column, Text,Date, Integer, String, DateTime, ARRAY, Time, Numeric, Table, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship, backref

from anime_scraper import settings

DeclarativeBase = declarative_base()
Base = DeclarativeBase

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

anime_cast_table = Table('anime_cast_table', Base.metadata,
                    Column("anime_id", Integer, ForeignKey('animes.id')),
                    Column("character_id", Integer, ForeignKey('characters.id'))
                    )

movie_cast_table = Table('movie_cast_table', Base.metadata,
                    Column("movie_id", Integer, ForeignKey('movies.id')),
                    Column("character_id", Integer, ForeignKey('characters.id'))
                    )


class Anime(DeclarativeBase):  # anime is entity type and calling-out is entity, title is attribute type
    """ c """
    __tablename__ = 'animes'
    #unique fields
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    alt_title = Column('alt_title', String, nullable=True)
    thumbnail_url = Column('thumbnail_url', String, nullable=True)
    preview_url = Column('preview_url', String, nullable=True)
    no_of_episodes = Column('no_of_episodes', Integer, nullable=True)
    description = Column('description', Text(), nullable=True)
    gallary_urls = Column("gallary_urls", ARRAY(String), nullable=True)
    rank = Column("rank",Integer, nullable=True)
    anime_reviews = Column("anime_reviews", ARRAY(String), nullable=True)
    #repetative fields
    
    studio_id = Column(Integer, ForeignKey('studios.id'))

    characters = relationship("Character",secondary=anime_cast_table, backref='animes', cascade_backrefs=False)

    release_date_id = Column(Integer, ForeignKey('releasedates.id'))

    rating_id = Column(Integer, ForeignKey('ratings.id'))

    

class Character(DeclarativeBase):
    """ c """
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    alt_name = Column('alt_name', String, nullable=True)
    gender = Column('gender', Enum('Male', 'Female', 'Trans-M', 'Trans-F', 'Intersex', name='gender_type'))
    description = Column('description', Text(), nullable=True)
    profile_pic = Column('profile_pic', ARRAY(String))
    hair_color = Column('hair_color', String)
    rank = Column('character_rank', Integer)

    #repetative fields
    rating_id = Column(Integer, ForeignKey('ratings.id'))

    #animes = relationship("Anime", secondary=anime_cast_table, backref='characters', cascade_backrefs=False)

    #movies = relationship("Movie", secondary=movie_cast_table, backref='characters', cascade_backrefs=False)


class ReleaseDate(DeclarativeBase):
    """ c """
    __tablename__ = 'releasedates'

    id = Column(Integer, primary_key=True)
    release_date = Column('relesse_date', Date, unique=True)

    animes = relationship("Anime", backref='release_date', cascade_backrefs=False)

    movies = relationship("Movie", backref='release_date', cascade_backrefs=False)


class Rating(DeclarativeBase):
    """ c """
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    rating = Column('rating', Numeric, unique=True)

    characters =relationship("Character", backref = "rating", cascade_backrefs=False)

    animes = relationship("Anime", backref='rating', cascade_backrefs=False)

    movies = relationship("Movie", backref='rating', cascade_backrefs=False)


class Movie(DeclarativeBase):
    """ Movie Model """
    __tablename__ = 'movies'
    #unique fields
    id = Column(Integer, primary_key=True)
    movie_title = Column('movie_title', String)
    movie_cover = Column('movie_cover', ARRAY(String))
    length = Column('length', Time)
    movie_trailer = Column('movie_trailer', String, nullable=True)
    description = Column('description', Text(), nullable=True)
    gallary_urls = Column("gallary_urls", ARRAY(String), nullable=True)
    #repetitive fields
    studio_id = Column(Integer, ForeignKey('studios.id'))

    characters = relationship("Character", secondary=movie_cast_table, backref='movies')

    release_date_id = Column(Integer, ForeignKey('releasedates.id'))

    rating_id = Column(Integer, ForeignKey('ratings.id'))



class Studio(DeclarativeBase):
    """ c """
    __tablename__ = 'studios'

    id = Column(Integer, primary_key=True)
    studio = Column('studio', String, unique=True)
    despcription = Column('description', Text(), nullable=True)
    #repetative fields

    movies = relationship("Movie", backref="studio", cascade_backrefs=False)

    animes = relationship("Anime", backref="studio", cascade_backrefs=False)



