from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from ..core.multiparts import SpeechboxMultipartParser


async def route_wp_log(request: Request) -> Response:
    # Read request stream (SpeechUX log)
    #body = b''
    #async for chunk in request.stream():
    #    body += chunk

    return Response(None, 204)


async def route_wp_query(request: Request) -> Response:
    # Parse query parameters
    install_id = request.query_params.get('installid')
    session_id = request.query_params.get('sessionid')
    request_id = request.query_params.get('requestid')

    version = request.query_params.get('version')
    locale = request.query_params.get('locale')
    grammars = request.query_params.get('grammars')
    test = request.query_params.get('test')

    client = request.query_params.get('client')
    client_version = request.query_params.get('clientversion')

    device_os = request.query_params.get('device.os')
    device_os_version = request.query_params.get('device.os.version')
    device_type = request.query_params.get('device.type')
    device_make = request.query_params.get('device.make')
    device_model = request.query_params.get('device.model')

    # Print the device information
    print('-- vv ----- POST WP QUERY ----------------------------------------')
    print('   Version: {0} | Locale: {1} | Test: {2}'.format(version, locale, test))
    print('   Install ID : {0}'.format(install_id))
    print('   Session ID : {0}'.format(session_id))
    print('   Request ID : {0}'.format(request_id))
    print('   Grammars   : {0}'.format(grammars))
    print('   Client     : {0} {1}'.format(client, client_version))
    print('   Device     : {0} {1} {2} on {3} {4}'.format(device_type, device_make, device_model, device_os, device_os_version))
    print('-- ^^ ----- POST WP QUERY ----------------------------------------')

    if not request_id:
        return Response('No "requestid" query parameter was provided.', 400)

    # Read request stream and parse multipart (audiobytes)
    parser = SpeechboxMultipartParser(request.stream())
    audio = await parser.parse()

    print('-- Got audio: {0}'.format(audio))

    # "version":
    # - MUST be "2.0"!
    # 
    # "status":
    # - "success": Successful recognition, do something with "name" value.
    # - "false reco": Error with "Sorry, didn't catch that.".
    # 
    # "name", "lexical":
    # - Tags:
    #   <profanity>Something</profanity> to censor text in it.
    #   <prosody volume='silent'>Whatever</prosody> to ???.
    response = {
        "version": "2.0",
        "header": {
            "status": "success",
            "name": "Hello, World!",
            "lexical": "Hello, World!",
            "properties": {
                "requestid": request_id
            }
        },
        "results": []
    }

    return JSONResponse(response, 200)
