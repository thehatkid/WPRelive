from urllib.parse import quote
from aiofiles.ospath import exists
from starlette.requests import Request
from starlette.responses import Response, FileResponse

__all__ = ("route_get_today_image",)


async def route_get_today_image(request: Request) -> Response:
    """Bing search Today Image service endpoint.

    Returns
    -------
    200:
        Returns "OK" status with a image file in body.
        The file must be image/jpg.
    304:
        Returns "Not Modified" status with empty body if `If-None-Match` header
        matches with current (ETag) hashed file.
    """

    # Date of image
    # E.g. 0 (-0) is today, 1 is yesterday, 4 means getting the image
    # from 4 days ago, and so on.
    offset = request.query_params.get("dateOffset", "0")

    # Market code to get localized image and hotpoints
    mkt = request.query_params.get("mkt", "en-US")

    # Screen (image) resolution
    # E.g. 480x800, 800x480 (WVGA), 1024x768, 768x1024 (WXGA)
    # Note that client may request twice to get portrait and landscape image
    orientation = request.query_params.get("orientation")

    url_encode_headers = request.query_params.get("urlEncodeHeaders")  # bool
    os_name = request.query_params.get("osName")
    os_version = request.query_params.get("osVersion")
    device_name = request.query_params.get("deviceName")
    application_id = request.query_params.get("AppId")
    user_id = request.query_params.get("UserId")

    # Header values should be URL encoded. It can take some HTTP headers:
    # ETag: value used for caching image, copyright text and hotspots
    # Image-Info-Credit: used to display copyright text
    # Image-Info-Hotspot-#: used to provide hotspots, can have up to 4

    # Hotspots are image overlay things that can have text, description,
    # and search query. Hotspot information is formatted as four strings,
    # joined with semicolon (;).
    # E.g. "Here's Johnny!;generic;...wait, wrong door;do a barrel roll;;"
    #
    # TODO: Document leftover of Hotspot information
    # Format: "text_1;type;text_2;query;;"
    # text_1: Primary text
    # type: Search type, can be:
    # - "generic" (web pane)
    # - "images" (images pane)
    # - "maps" (TODO undocumented)
    # - "videos" (???)
    # - "reference" (web pane)
    # text_2: Secondary text
    # query: Search query text
    #
    # Unused on WP7 but returned by service:
    # Expires: expiration date of image, could be the date until next day
    # Image-Info-Logo: 1(?), takes integer
    # Image-Info-Glass: 15(?), takes integer

    # JPG image file
    filename = "./static/todayimage/someday.jpg"
    if orientation:
        if await exists(f"./static/todayimage/someday_{orientation}.jpg"):
            filename = f"./static/todayimage/someday_{orientation}.jpg"
        else:
            print(f"Could not get Today Image for '{orientation}'")

    # Caching
    etag = "deadc0ffee"
    if request.headers.get("If-None-Match") == etag:
        return Response(None, 304)

    headers = {
        "ETag": etag,
        "Image-Info-Credit": quote(
            "\"Someday\" \u00A9 Alena Aenami\nhat_kid was here :3"
        ),
        "Image-Info-Hotspot-1": quote(
            "Home back home...;generic;Something is familiar here;hello world;;"
        ),
        "Image-Info-Hotspot-2": quote(
            "Hmm...;images;Could be perfect image to your collection;alena aenami someday;;"
        ),
    }

    return FileResponse(filename, 200, headers)
