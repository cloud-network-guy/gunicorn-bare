import traceback
import json

def application(environ, start_response):

    try:

        # Create a standard WSGI response with HTTP 200 code
        http_response = {
            'statusCode': "200 OK",
            'headers': [("Content-Type", "application/json")],
            'body': json.dumps({"message": "Hello there"}),
        }

    except Exception as e:

        # Return a 500 status code with the error message in plain text
        http_response = {
            'statusCode': "500 Internal Server Error",
            'headers': [('Content-type', "text/plain")],
            'body': traceback.format_exc(),
        }

    # Start the WSGI response with code and headers
    response_status = http_response.get('statusCode', "000 Unknown")
    response_headers = http_response.get('headers', [])
    start_response(response_status + " ", response_headers)

    if body := http_response.get('body'):
        # If response body is string, we must encode it to bytestring
        return [body.encode('utf-8') if isinstance(body, str) else body]
    
    return []

