def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.make_response>`.
    """
    
    # Returns a dictionary
    request_args = request.args

    # If the dictionary contains any name key to it, then we extract the value and store on name
    if request.args and 'name' in request.args:
        name = request_args['name']
    else:
        name = "World"
    return f'Hello {name}!'
