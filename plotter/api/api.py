from datetime import datetime

from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from plotter.database.core import (
    insert_points as db_insert_points,
    delete_all_points as db_delete_all_points, fetch_points_for_chart
)
from plotter.api.models import Point
from plotter.database.dbo import PointDBO
from plotter.plot import create_plot_from_points

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/insert-points", status_code=201)
def insert_points(items: list[Point]) -> dict[str, str]:
    if items:
        db_insert_points(map(lambda item: PointDBO(**item.dict()), items))

    return {'message': f'Successfully inserted {len(items)} items'}


@router.delete("/delete-all-points", description="Deletes all tracked points from database")
def delete_all_points() -> dict[str, str]:
    deleted_count = db_delete_all_points()
    return {'message': f'Successfully deleted {deleted_count} items'}


@router.get("/chart", response_class=HTMLResponse)
def chart(request: Request) -> Response:
    db_points = fetch_points_for_chart()
    chart_base64_img = create_plot_from_points(db_points.points)

    return templates.TemplateResponse("chart.html", {
        "request": request,
        "chart_base64": chart_base64_img,
        "point_datetime": datetime.fromtimestamp(db_points.inserted_at) if db_points.inserted_at else None
    })
