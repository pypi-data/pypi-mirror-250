from fastapi import APIRouter, FastAPI

from mlbull.exceptions import NotValidPackageException
from .log_routes import get_logs_router

from .notebooks import get_notebook_as_module
from .utils import (
    get_decorators,
    get_module_from_filename,
    sanitize_module_name,
)
from os import getcwd, chdir
from pathlib import Path

from logging import getLogger

logger = getLogger(__name__)


def generate_router(filename: str):
    current_directory = getcwd()
    path = Path(filename)
    target_directory = path.parent
    chdir(target_directory)
    try:
        if filename.endswith(".py"):
            module, logger = get_module_from_filename(path.name, str(path))
            notebook_html = None
        elif filename.endswith(".ipynb"):
            module, logger, notebook_html = get_notebook_as_module(
                path.name, str(path)
            )
        else:
            raise NotValidPackageException(
                f"{filename} is not something that looks like python"
            )
        functions = get_decorators(module)

        sanitized_name = sanitize_module_name(module.__name__)
        router = APIRouter(prefix=f"/{sanitized_name}", tags=[filename])

        log_router = get_logs_router(logger, notebook_html)

        router.include_router(log_router, prefix="/meta")

        for function in functions:
            router.post(f"/{function.__name__}")(function)

        return router
    finally:
        chdir(current_directory)


def add_routers(app: FastAPI, directory: str):
    path = Path(directory)
    for file in path.iterdir():
        if file.name.startswith("__"):
            continue
        try:
            router = generate_router(file.__str__())
            app.include_router(router)
        except NotValidPackageException:
            logger.error(f"Failed to import {file}, not valid target")
        except ModuleNotFoundError as e:
            logger.error(f"Failed to import {file}, {e.msg}")
