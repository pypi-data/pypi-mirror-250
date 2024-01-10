from typing import Optional, Tuple, Dict
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, HTMLResponse
from .print_logger import PrintLogger


def get_logs_router(print_logger: PrintLogger, notebook_html: Optional[str]):
    router = APIRouter()

    @router.get("/logs", response_class=PlainTextResponse)
    def view_logs() -> str:
        return print_logger.get_logged_data()

    if notebook_html is not None:

        @router.get("/notebook", response_class=HTMLResponse)
        def view_notebook():
            return notebook_html

    return router
