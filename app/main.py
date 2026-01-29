from fastapi import FastAPI

from backend.app.api import init_api
from backend.app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.project_name)
    init_api(app)
    return app


app = create_app()

