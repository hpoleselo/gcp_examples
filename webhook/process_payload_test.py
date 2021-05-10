import json

with open('payload.json') as json_data:
    data = json.load(json_data)

# To get content from the API
# Here we're just retrieving the Payload from the Webhook (which file has been changed)
# Maybe we can track an specific folder using Git's REST API
# https://docs.github.com/en/rest/reference/repos#contents
print(data['head_commit']['added'])
