from fastapi.responses import RedirectResponse


def redirect_to_docs():
    return RedirectResponse("/docs")
