# Command to run this function: functions-framework --target hello_world

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

    # We're going to add the functionality to handle the data when it comes as JSON (since we're using Postman to post the JSON payload)
    # Remembering we cannot pass JSON in the URL but we can in Postman
    request_json = request.get_json(silent=True)

    # If the dictionary contains any name key to it, then we extract the value and store on name
    if request.args and 'name' in request.args and 'lastname' in request.args:
        name = request_args['name']
        lastname = request_args['lastname']
    elif request_json and 'name' in request_json and 'lastname' in request_json:
        name = request_json['name']
        lastname = request_json['lastname']
    else:
        name = "World"
    return f'Hello {name} {lastname}!'
