import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date

database_path = os.environ["DATABASE_URL"]
if database_path and database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


actor_in_movie = db.Table(
    'actor_in_movie',
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True)
)


class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    release_date = Column(Date, nullable=False)
    imdb_rating = Column(Float, nullable=False)
    cast = db.relationship('Actor', secondary=actor_in_movie,
                           backref='movies', lazy=True)

    def __init__(self, title, release_date, imdb_rating):
        self.title = title
        self.release_date = release_date
        self.imdb_rating = imdb_rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.strftime("%B %d, %Y")
        }

    def long(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.strftime("%B %d, %Y"),
            "imdb_rating": self.imdb_rating
        }

    def full_info(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.strftime("%B %d, %Y"),
            "imdb_rating": self.imdb_rating,
            "cast": [actor.name for actor in self.cast]
        }

    def __repr__(self):
        return f"<Movie {self.id} {self.title} {self.release_date} {self.imdb_rating} {self.cast}/>"


class Actor(db.Model):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    date_of_birth = Column(Date, nullable=False)

    def __init__(self, name, date_of_birth):
        self.name = name
        self.date_of_birth = date_of_birth

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def long(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_of_birth": self.date_of_birth.strftime("%B %d, %Y")
        }

    def full_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_of_birth": self.date_of_birth.strftime("%B %d, %Y"),
            "movies": [movie.title for movie in self.movies]
        }

    def __repr__(self):
        return f"<Actor {self.id} {self.name} {self.date_of_birth}/>"
