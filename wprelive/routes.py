from starlette.routing import Mount, Route
from starlette.requests import Request
from starlette.responses import Response

from .api import speechrecognition, bing, bgimage

__all__ = (
    "route_index",
    "speechreco_routes",
    "searchsvc_routes",
    "backgroundimagesvc_routes",
    "routes",
)


async def route_index(request: Request) -> Response:
    return Response(None, 404)


speechreco_routes = [
    Route(
        "/wp/log",
        speechrecognition.route_wp_log,
        methods=["POST"],
        name="speechreco_log",
    ),
    Route(
        "/wp/query",
        speechrecognition.route_wp_query,
        methods=["POST"],
        name="speechreco_query",
    ),
]

# Services
searchsvc_routes = [
    Route(
        "/Search.svc/{type:str}/",
        bing.route_search,
        methods=["POST"],
        name="search_svc",
    ),
]
backgroundimagesvc_routes = [
    Route(
        "/TodayImageService.svc/GetTodayImage",
        bgimage.route_get_today_image,
        methods=["GET"],
        name="todayimage_svc",
    ),
]

routes = [
    Route("/", route_index, methods=[], name="index"),
    Mount("/speechreco", routes=speechreco_routes, name="speechreco"),
    Mount("/SearchService", routes=searchsvc_routes, name="SearchService"),
    Mount(
        "/BackgroundImageService",
        routes=backgroundimagesvc_routes,
        name="BackgroundImageService",
    ),
]
