from starlette.requests import Request
from starlette.responses import Response

__all__ = (
    "handler_not_found",
    "exception_handlers",
)


async def handler_not_found(request: Request, exception: Exception) -> Response:
    return Response(None, 404)


exception_handlers = {
    404: handler_not_found,
}
