from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from Controller.movie_controller import MovieController
from fastapi.staticfiles import StaticFiles
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="View/static"),  # dokładnie tak jak na screenie
    name="static"
)

@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    view: str = "list",
    id: int | None = None,
    db: Session = Depends(get_db),
):
    return MovieController.index(request=request, view=view, id=id, db=db)


@app.post("/add")
def add_movie(
    title: str = Form(...),
    year: int = Form(...),
    genre: str = Form(...),
    db: Session = Depends(get_db),
):
    return MovieController.add_movie(title=title, year=year, genre=genre, db=db)


@app.post("/edit/{movie_id}")
def edit_movie(
    movie_id: int,
    title: str = Form(...),
    year: int = Form(...),
    genre: str = Form(...),
    db: Session = Depends(get_db),
):
    return MovieController.update_movie(
        movie_id=movie_id,
        title=title,
        year=year,
        genre=genre,
        db=db,
    )


@app.post("/delete/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
):
    return MovieController.delete_movie(movie_id=movie_id, db=db)
