from starlette.routing import Mount, Route
from starlette.requests import Request
from starlette.responses import Response

from .api import speechrecognition, bing


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

searchsvc_routes = [
    Route(
        '/Search.svc/{type:str}/',
        bing.route_search,
        methods=['POST'],
        name='searchservice_svc'
    )
]

routes = [
    Route('/', route_index, methods=[], name='index'),
    Mount('/speechreco', routes=speechreco_routes, name='speechreco'),
    Mount('/SearchService', routes=searchsvc_routes, name='searchservice')
]
