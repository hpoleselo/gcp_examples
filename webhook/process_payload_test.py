import json
import requests
import os
from pprint import pprint
from github import Github


def get_repo_content():
    """ Uses Github API module to retrieve content from repo.
    Good reference for it: https://pygithub.readthedocs.io/en/latest/github_objects/ContentFile.html#github.ContentFile.ContentFile """

    token = os.getenv('GITHUB_TOKEN', '...')
    file_path = "webhook"
    g = Github(token)
    repo = g.get_repo("hpoleselo/gcp-etl")

    files = repo.get_contents(file_path, ref="master")
    
    for file in files:
        if file.name == 'process_payload_test.py':
            print(f'Decoding content from: {file.name}')
            print(file.decoded_content.decode("utf-8"))

    # If we wanted to change the data
    #data += "\npytest==5.3.2"


def get_repo_issues():
    """ Using Github REST API, with the generated token on https://github.com/settings/tokens, retrieving repo's issues.
    This assumes we have exported on the Shell session: export GITHUB_TOKEN='YOURTOKEN'
    Or just add to the .env file and source the .env file
    This function uses requests instead of the pygithub module. """

    token = os.getenv('GITHUB_TOKEN', '...')
    owner = "hpoleselo"
    repo = "TelegramForecaster"
    query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
        "state": "open",
    }
    headers = {'Authorization': f'token {token}'}
    r = requests.get(query_url, headers=headers, params=params)
    pprint(r.json())


def test_webhook_payload():
    with open('payload.json') as json_data:
        data = json.load(json_data)

    # Here we're just retrieving the Payload from the Webhook (which file has been changed)
    print(data['head_commit']['added'])


test_webhook_payload()
#get_repo_content()