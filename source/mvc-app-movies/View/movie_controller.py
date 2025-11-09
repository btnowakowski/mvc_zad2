from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from Model.movie_model import MovieModel
from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="views")

class MovieController:

    @staticmethod
    def index(request: Request, view: str, id: int | None, db: Session):
        model = MovieModel(db)

        if view == "list":
            movies = model.get_all()
            return templates.TemplateResponse(
                "movie_list.html",
                {"request": request, "movies": movies},
            )

        if view == "add":
            return templates.TemplateResponse(
                "add_movie.html",
                {"request": request},
            )

        if view == "edit":
            if id is None:
                raise HTTPException(status_code=400, detail="Brak parametru id")
            movie = model.get(id)
            if not movie:
                raise HTTPException(status_code=404, detail="Film nie istnieje")
            return templates.TemplateResponse(
                "edit_movie.html",
                {"request": request, "movie": movie},
            )

        raise HTTPException(status_code=404, detail="Nieznany widok")

    @staticmethod
    def add_movie(title: str, year: int, genre: str, db: Session):
        model = MovieModel(db)
        model.create(title=title, year=year, genre=genre)
        return RedirectResponse(url="/?view=list", status_code=303)

    @staticmethod
    def update_movie(movie_id: int, title: str, year: int, genre: str, db: Session):
        model = MovieModel(db)
        movie = model.update(movie_id, title, year, genre)
        if not movie:
            raise HTTPException(status_code=404, detail="Film nie istnieje")
        return RedirectResponse(url="/?view=list", status_code=303)

    @staticmethod
    def delete_movie(movie_id: int, db: Session):
        model = MovieModel(db)
        ok = model.delete(movie_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Film nie istnieje")
        return RedirectResponse(url="/?view=list", status_code=303)
