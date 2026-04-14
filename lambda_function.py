from traceback import format_exc
from base64 import b64encode
from main import process_request


# AWS Lambda Entry Point
def lambda_handler(event, context):

    # Log the incoming headers to CloudWatch
    print(event)

    request = {
        'path': event.get('path', '/'),
        'params': event.get('queryStringParameters', {}),
    }
    multi_value_headers = False
    
    try:
        # Parser event headers to get values to pass to main function
        if multi_value_headers := event.get('multiValueHeaders'):
            request['host'] = multi_value_headers['host'][0]
            for item in event["multiValueQueryStringParameters"].items():
                k, v = item
                request['params'][k] = str(v)
        else:
            request['host'] = event['headers']['host']

        response = process_request(request)

        # Start forming an HTTP response to send back to Lambda
        http_response = {'statusCode': response.get('statusCode', 000)}

        # Lambda requires headers be formatted in a Dictionary rather than List
        if multi_value_headers:
            headers_dict = {}
            for header in response.get('headers'):
                k = header[0]
                v = header[1]
                if headers_dict.get(k):
                    headers_dict[k].append(v)
                else:
                    headers_dict[k] = v
            http_response.update({'multiValueHeaders': headers_dict})
        else:
            headers = {k: v for k, v in response.get('headers')}
            http_response.update({'headers': headers})

        # Form Response Body
        if body := response.get('body'):
            if isinstance(body, str):
                http_response.update({'body': body})
            else:
                # Response was binary, so convert it to base-64 encoded
                http_response.update({
                    'isBase64Encoded': True,
                    'body': b64encode(body).decode("utf-8"),
                })
        else:
            http_response.update({'body': ""})  # Lambda can't handle NoneTypes

    except Exception as e:

        http_response = {'statusCode': 500, 'body': str(format_exc())}
        if multi_value_headers:
            http_response.update({'multiValueHeaders': {'Content-Type': ["text/plain"]}})
        else:
            http_response.update({'headers': {'Content-Type': "text/plain"}})

    # Log the outgoing response to CloudWatch
    print(http_response)

    # Return the response to Lambda
    return http_response
