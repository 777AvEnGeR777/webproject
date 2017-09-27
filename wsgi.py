def simple_app(environ, start_response):
    get_params = environ["QUERY_STRING"]
    body = 'Hello, World! By gunicorn\n'
    
    body += 'GET parameters:\n'
    body += parse(get_params)
	
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    post_params = environ['wsgi.input'].read(request_body_size)

    body += 'POST parameters:\n'
    body += parse(post_params)

    status = '200 OK'
    headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(body)))]	

    start_response(status, headers)
    return [ body ]

def parse(params):
    result = ''
    for val in params.split('&'):
        result += val + '\n'
    return result
