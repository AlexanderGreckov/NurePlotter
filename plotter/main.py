from fastapi import FastAPI

from plotter.api.api import router
from .database import close_db_connection


application = FastAPI(version='1.0.0')
application.include_router(router)


@application.on_event("shutdown")
def shutdown_event() -> None:
    close_db_connection()
