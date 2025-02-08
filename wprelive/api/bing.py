from starlette.requests import Request
from starlette.responses import Response, JSONResponse


async def route_search(request: Request) -> Response:
    # Could be: "json", "withnif", "jsonwithnif"
    # Usually uses "jsonwithnif"
    q_type = request.path_params.get('type', 'json')

    q_app_id = request.query_params.get('AppID')
    q_pc = request.query_params.get('PC')
    q_form = request.query_params.get('form')
    q_input = request.query_params.get('input')

    data = await request.json()

    context = data['Context']  # Dict
    properties = data['Properties']  # List
    queries = data['Queries']  # List

    print('Bing: Search for "{}"'.format(queries[0]['QueryString']))

    # TODO: Figure out how to respond to Bing Search application
    return JSONResponse([], 200)
