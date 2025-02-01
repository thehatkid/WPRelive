from starlette.routing import Mount, Route
from starlette.requests import Request
from starlette.responses import Response

from .api import speechrecognition


async def route_index(request: Request) -> Response:
    return Response(None, 404)


speechreco_routes = [
    Route(
        '/wp/log',
        speechrecognition.route_wp_log,
        methods=['POST'],
        name='speechreco_log'
    ),
    Route(
        '/wp/query',
        speechrecognition.route_wp_query,
        methods=['POST'],
        name='speechreco_query'
    )
]

routes = [
    Route('/', route_index, methods=[], name='index'),
    Mount('/speechreco', routes=speechreco_routes, name='speechreco')
]
