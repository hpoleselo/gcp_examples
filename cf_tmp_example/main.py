from github import Github, BadCredentialsException
from zipfile import ZipFile
from google.cloud import storage
from os import path, environ
from config import configuration

GITHUB_TOKEN = configuration['github_token']
is_local_testing = configuration['local_testing']

if is_local_testing:
    print("Running locally...")
    creds_path = r"C:\Users\HPOLESE1\Documents\MLOps Platform\ModelValidator\model_validator\mpv_creds.json"
    environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path

# Cloud Storage Client
storage_client = storage.Client()
bucket_name = 'cf_tmp_bucket'
bucket = storage_client.get_bucket(bucket_name) 

# Root path on CF will be /workspace, while on local Windows: C:\
root = path.dirname(path.abspath(__file__))

def parse_from_git(request):
    repo_path = '.'
    branch = 'master'
    repository_url = 'hpoleselo/gcs_test'
    try:
        git = Github(GITHUB_TOKEN)
        repo = git.get_repo(repository_url)
        repo_files = repo.get_contents(repo_path)
        zipped_files_path = '/tmp/zipped_files.zip'
        with ZipFile(path.join(root, zipped_files_path), 'w') as zipObject:
            print(f"Getting content from {repository_url} repository...")
            for file in repo_files:
                content = get_content_from_git(file)
                zip_path = '/tmp/' + file.name
                zip_path_f = path.join(root, zip_path)
                file_local = create_file(file.name, content)
                zipObject.write(zip_path_f, arcname=file.name)
        
        print("Content succesfully retrieved.")
        # ! When writing to GCS, C:\ is coming as well.
        push_to_gcs(path.join(root, zipped_files_path))
        return 'Files written to GCS.', 200
    except BadCredentialsException:
        print("Bad credentials, check if your token is valid.")
        return 'Could not get files from GitHub, bad credentials.', 204

def get_content_from_git(file):
    """ Decodes file from GitHub. """
    content = file.decoded_content.decode('utf-8')
    return content

def create_file(file_name, file_content):
    """ Creates a file on runtime. """
    file_path = '/tmp/' + file_name
    file_path = path.join(root, file_path)

    # If file is a binary, we rather use 'wb' instead of 'w'
    with open(file_path, 'w') as file:
        file.write(file_content)

def push_to_gcs(file):
    """ Writes to Google Cloud Storage. """
    file_name = file.split('/')[-1]
    print(f"Pushing {file_name} to GCS...")
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file)
    print(f"File pushed to {blob.id} succesfully.")