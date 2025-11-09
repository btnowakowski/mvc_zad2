from typing import Optional

from fastapi import Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from Model.movie_model import MovieModel

templates = Jinja2Templates(directory="View")


class MovieController:
    """Warstwa kontrolera: przyjmuje requesty, gada z Modelem, zwraca View."""

    @staticmethod
    def index(
        request: Request,
        view: str = "list",
        id: Optional[int] = None,
        db: Session = Depends(get_db),
    ) -> HTMLResponse:
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
    def add_movie(
        title: str = Form(...),
        year: int = Form(...),
        genre: str = Form(...),
        db: Session = Depends(get_db),
    ):
        model = MovieModel(db)
        model.create(title=title, year=year, genre=genre)
        return RedirectResponse(url="/?view=list", status_code=303)

    @staticmethod
    def update_movie(
        movie_id: int,
        title: str = Form(...),
        year: int = Form(...),
        genre: str = Form(...),
        db: Session = Depends(get_db),
    ):
        model = MovieModel(db)
        movie = model.update(movie_id, title, year, genre)
        if not movie:
            raise HTTPException(status_code=404, detail="Film nie istnieje")
        return RedirectResponse(url="/?view=list", status_code=303)

    @staticmethod
    def delete_movie(
        movie_id: int,
        db: Session = Depends(get_db),
    ):
        model = MovieModel(db)
        ok = model.delete(movie_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Film nie istnieje")
        return RedirectResponse(url="/?view=list", status_code=303)
