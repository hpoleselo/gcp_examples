def on_repo_change(request):
    """ Function to be called whenever one pull is made to the repo.
    Args:
      HTTP Request
    Return:
      List of the item(s) added to the repo
    """

    # We're going to add the functionality to handle the data when it comes as JSON (since we're using Postman to post the JSON payload)
    # Remembering we cannot pass JSON in the URL but we can in Postman
    request_json = request.get_json()

    #  Get only recent added files from payload
    added_files = request_json['head_commit']['added']

    if len(added_files) > 0:
        for file_name in added_files:
            print(f'{file_name} was added on the repo.')
        return f'Recent pushed files have been detected. Files: {added_files}'
    else:
        return 'Not Okay'
