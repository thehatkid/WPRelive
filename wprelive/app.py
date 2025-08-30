from starlette.applications import Starlette

from .routes import routes
from .handlers import exception_handlers

__all__ = ("app",)

app = Starlette(
    debug=False,
    routes=routes,
    exception_handlers=exception_handlers,
)
