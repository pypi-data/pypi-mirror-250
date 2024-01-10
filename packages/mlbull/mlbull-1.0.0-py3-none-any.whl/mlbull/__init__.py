from fastapi import FastAPI

from mlbull.generate_router import add_routers
from .doc_router import redirect_to_docs

from os import environ


app = FastAPI(title="MLbull")

app.get("/")(redirect_to_docs)

add_routers(app, environ["MODEL_DIRECTORY"])
