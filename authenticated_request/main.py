from flask import abort
import os

def get_bearer_token(request):
    """ Retrieves the bearer token that we placed on our Postman POST request header. Remembering that the request is
    """

    # Gets the Header portion of the request, if it has authorization, we'll proceed.
    bearer_token = request.headers.get('Authorization', None)

    if not bearer_token:
        abort(401, 'Bearer token field is empty.')
    parts = bearer_token.split()
    if parts[0].lower() != "bearer":
        abort(401, 'Authorization header has to start with Bearer')
    elif len(parts) == 1:
        abort(401, 'Token was not found.')
    elif len(parts) > 2:
        abort(401, 'Authorization header must be in the form of Bearer token')
    bearer_token = parts[1]
    return bearer_token

def hello_world(request):
    """ Function to be called whenever one pull is made to the repo.
    Args:
      HTTP Request
    Return:
      Message saying which kind of push has been made and which files were added/modified/removed
    """


    # Has to be a POST method in order to the function to be executed
    if request.method != 'POST':
        abort(405, 'Request must be a POST method.')
    
    bearer_token = get_bearer_token(request)
    secret_key = os.environ.get('ACCESS_TOKEN')
    if bearer_token != secret_key:
        abort(401, 'Invalid bearer token provided.')

    # The context type inside the body response is JSON, so makes sense to get_json()
    request_json = request.get_json()

    # If the dictionary contains any name key to it, then we extract the value and store on name
    if request.args and 'name' in request.args and 'lastname' in request.args:
        name = request_args['name']
        lastname = request_args['lastname']
    elif request_json and 'name' in request_json and 'lastname' in request_json:
        name = request_json['name']
        lastname = request_json['lastname']
    else:
        name = "World"
        lastname = "!"
    return f'Hello {name} {lastname}'
