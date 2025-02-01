from starlette.applications import Starlette

from .routes import routes
from .handlers import exception_handlers

app = Starlette(
    debug=False,
    routes=routes,
    exception_handlers=exception_handlers
)
