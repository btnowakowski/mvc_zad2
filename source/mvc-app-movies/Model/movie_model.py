from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String(100), nullable=False)


class MovieModel:
    """Logika dostępu do danych (Model w MVC)."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Movie).order_by(Movie.id.desc()).all()

    def get(self, movie_id: int):
        return self.db.query(Movie).filter(Movie.id == movie_id).first()

    def create(self, title: str, year: int, genre: str):
        movie = Movie(title=title, year=year, genre=genre)
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def update(self, movie_id: int, title: str, year: int, genre: str):
        movie = self.get(movie_id)
        if not movie:
            return None
        movie.title = title
        movie.year = year
        movie.genre = genre
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete(self, movie_id: int):
        movie = self.get(movie_id)
        if not movie:
            return False
        self.db.delete(movie)
        self.db.commit()
        return True
