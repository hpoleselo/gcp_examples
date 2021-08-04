from github import Github
from zipfile import ZipFile
from google.cloud import storage
from os import path, environ

GITHUB_TOKEN = ''

# Uncomment this when running locally to use credentials from the Service Account
#creds_path = r"C:\Users\ABSOLUTE_PATH_TO_YOUR_SEVICE_ACCOUNT_CREDENTIALS\gcp_creds.json"
#environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path

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
    git = Github(GITHUB_TOKEN)
    repo = git.get_repo(repository_url)
    repo_files = repo.get_contents(repo_path)
    zipped_files_path = '/tmp/zipped_files.zip'
    with ZipFile(path.join(root, zipped_files_path), 'w') as zipObject:
        for file in repo_files:
            content = get_content_from_git(file)
            zip_path = '/tmp/' + file.name
            zip_path_f = path.join(root, zip_path)
            file_local = create_file(file.name, content)
            zipObject.write(zip_path_f, arcname=file.name)

    # ! When writing to GCS, C:\ is coming as well.
    write_to_gcs(path.join(root, zipped_files_path))

    return 'Files written to GCS', 200

def get_content_from_git(file):
    content = file.decoded_content.decode('utf-8')
    return content

def create_file(file_name, file_content):
    file_path = '/tmp/' + file_name
    file_path = path.join(root, file_path)

    # If file is a binary, we rather use 'wb' instead of 'w'
    with open(file_path, 'w') as file:
        file.write(file_content)

def write_to_gcs(file):
    """ Writes to Google Cloud Storage. """
    blob = bucket.blob(file)
    blob.upload_from_filename(file)