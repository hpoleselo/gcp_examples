import os


secret_id = os.environ.get('secret_id', 'Could not retrieve environment variable.')
project_id = os.environ.get('project_id', 'Could not retrieve environment variable.')

request = {'name': f'projects/{project_id}/secrets/{secret_id}/'}

# When deploying the function:
# gcloud functions deploy auth_hook_test --runtime python38 --env-vars-file env_metadata.yaml --trigger-http


def secret_manager_test(request):
    print("Test")
    print(secret_id)
    print(project_id)
    return secret_id, 200