from sqlalchemy import Column, String, Integer, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from utilities.sqlalchemy_setup import Base
from enum import Enum as PyEnum

class Movie(Base):
    __tablename__ = 'movies'
    show_id = Column(String(10), primary_key=True)
    type = Column(String(10))
    title = Column(String(255))
    director = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    date_added = Column(Date, nullable=True)
    release_year = Column(Integer)
    rating = Column(String(10))
    duration = Column(Integer)
    description = Column(String(255), nullable=True)

    actors = relationship('ShowActor', back_populates='movie')
    genres = relationship('ShowGenre', back_populates='movie')
    

class Actor(Base):
    __tablename__ = 'actors'
    actor_id = Column(Integer, primary_key=True, autoincrement=True)
    actor_name = Column(String(255), nullable=False)

    shows = relationship('ShowActor', back_populates='actor')

class ShowActor(Base):
    __tablename__ = 'show_actors'
    show_id = Column(String(10), ForeignKey('movies.show_id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('actors.actor_id'), primary_key=True)

    movie = relationship('Movie', back_populates='actors')
    actor = relationship('Actor', back_populates='shows')

class Genre(Base):
    __tablename__ = 'genres'
    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    genre_name = Column(String(255), nullable=False)

    shows = relationship('ShowGenre', back_populates='genre')

class ShowGenre(Base):
    __tablename__ = 'show_genres'
    show_id = Column(String(10), ForeignKey('movies.show_id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.genre_id'), primary_key=True)

    movie = relationship('Movie', back_populates='genres')
    genre = relationship('Genre', back_populates='shows')

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    user_type = Column(String(10), nullable=False)

    watchlist = relationship('Watchlist', back_populates='user')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'user_type': self.user_type
        }

class WatchStatusEnum(PyEnum):
    watching = 'watching'
    plan_to_watch = 'plan_to_watch'
    finished = 'finished'

class Watchlist(Base):
    __tablename__ = 'watchlist'
    watchlist_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    show_id = Column(String(10), ForeignKey('movies.show_id'))
    status = Column(Enum(WatchStatusEnum))

    user = relationship('User', back_populates='watchlist')
    movie = relationship('Movie')
