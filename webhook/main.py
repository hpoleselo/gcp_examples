def on_repo_change(request):
    """ Function to be called whenever one pull is made to the repo.
    Args:
      HTTP Request
    Return:
      Message saying which kind of push has been made and which files were added/modified/removed
    """

    # The context type inside the body response is JSON, so makes sense to get_json()
    request_json = request.get_json()

    #  Get only recent added files from payload or modified files
    added_files = request_json['head_commit']['added']
    modified_files = request_json['head_commit']['modified']
    removed_files = request_json['head_commit']['removed']

    if added_files:
        for file_name in added_files:
            print(f'{file_name} was added on the repo.')
        return f'Recent pushed files have been detected. Files: {added_files}'
    elif modified_files:
        for file_name in modified_files:
            print(f'{file_name} was modified on the repo.')
        return f'Recent modified pushed files have been detected. Files: {modified_files}'
    else:
        for file_name in added_files:
            print(f'{file_name} was removed from the repo.')
        return f'Recent removed files from the repo have been detected. Files: {removed_files}'
