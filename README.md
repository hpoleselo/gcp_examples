### Reference

Cloud Run: setup runtime environment/packages and so on

When running cloud functions using Firebase service or similar, we have to use the credentials, in my case I created an alias to source the env. variable:

` $ gcpenv`

 ``` $ functions-framework --target hello_world --debug```

``` $ gcloud functions deploy set_expense --runtime python38 --trigger-http ```

Schedule a cloud function:

` $ gcloude components install beta`

`$ gcloud components update`

`$ gcloud topics create TOPIC_NAME `

``` $ gclou pubsub subscriptions create cron-sub --topic TOPIC_NAME ```

Deleting cloud functions:

` $ gcloud functions delete FUNCTION_NAME`

### GCP on Ubuntu

Followed this tutorial
https://cloud.google.com/sdk/docs/install#deb

After following it, initialize gcloud on the CLI (and authenticating it on your pc)

$ gcloud init

CLI Cheatsheet https://itnext.io/gcp-command-line-cheatsheet-5e4434ca2c84

Check if you're on your project and so on:
$ gcloud info 

In order to test our gcloud functions locally we have to install the `functions-framework`, which basically has Flask under the hood and emulates the Gcloud environment to run our functions locally before deploying to the Cloud.


### Running First Example (Ubuntu)

Access our virtual environment by using our alias: $ py-env, which activates the venv. Then:

```$ pip install -r requirements.txt```

For each function I think we would create a folder containing that function, because if you stop to think about it, every Gcloud Function has to be named main.py, so we have to separate that.

Before running the first example we have to activate the Cloud Build API since we're using Python and HTTP requests, for that, go to this link.

FOLLOW THIS LINK BEFORE ANYTHING:

https://cloud.google.com/functions/docs/quickstart-python?hl=pt-br

Maybe grant access from Cloud Build to use other services:https://console.cloud.google.com/cloud-build/settings

Create a main.py file (HAS TO BE NAMED THIS WAY, OTHERWISE GCLOUD WON'T RECOGNIZE IT), and the function

To test our function:

``` $ functions-framework --target hello_world```

Now go to a browser, follow the link of the localhost the Flask application created and you should see the output. In order to pass arguments for a request we use the `?`, so in the URL field on our browser we should:

```0.0.0.0:8080/?name=henrivis```

And click enter, it should refresh and we should see: `Hello henrivis!` as output.

After testing it using functions-framework, if we wanted to deploy our serverless function to GCP: 

`$ gcloud beta functions deploy hello_world --runtime python38 --trigger-http`

Now you should see on the terminal a big output, which basically gives your details about this deployment. Main fields should be:

```
entryPoint: hello_world
deployment-tool: cli-gcloud
runtime: python37
...
status: ACTIVE
timeout: 60s
updateTime: '2021-04-22T13:03:25.884Z'
versionId: '9'
```

So this is the 9th time we're deploying this function, timeout we could change if we wanted (on the console). Now you should be able to check on Cloud Functions (clicking on the function and checking the source code that it matches with the one that you have locally), to run the function just go the "Testing" tab and test the function.

Go to this URL and see that the function you deployed takes 256 MiB (Python)
https://console.cloud.google.com/functions/list

### Firestore to trigger Google Functions
Read about events and triggers:
https://cloud.google.com/functions/docs/concepts/events-triggers#functions_parameters-python
Then Implementation
https://cloud.google.com/functions/docs/calling/cloud-firestore#functions_firebase_firestore-python



### GCP on Docker

Instead of installing GCP tools locally, we're using Docker. Our main goal here is to run a simple serveless function driven by a http request.

To do that we have to install Cloud SDK to execute the gcloud commands:

`$ docker pull gcr.io/google.com/cloudsdktool/cloud-sdk:latest`

Test if image is working correctly:

`$ docker run gcr.io/google.com/cloudsdktool/cloud-sdk:slim gcloud version`

Authenticate with gcloud:

`$ docker run -ti --name gcloud-config gcr.io/google.com/cloudsdktool/cloud-sdk:slim gcloud auth login`

Now the authentication is saved under the gcloud_config container, docker ps -a if you will.

Verify the projects:

`$ docker run --rm --volumes-from gcloud-config gcr.io/google.com/cloudsdktool/cloud-sdk:slim gcloud compute instances list --project your_project`

`$ gcloud beta functions deploy hello_world --runtime python38 --trigger-http`

docker run --rm gcr.io/google.com/cloudsdktool/cloud-sdk:slim gcloud beta functions deploy load_data --runtime python38 --trigger-http


https://cloud.google.com/sdk/docs/downloads-docker#docker_image_options


### PostgresSQL on Docker

We're pulling postgres image direct from DockerHub instead of installing it locally in our computer, using db-env file to import user settings to access the database and mapping databases created in postgreSQL to our host PC to persist the data we're working with.

Run PostgreSQL db service from our docker-compose:

`$ docker-compose up`

Access postgres within the running container (Run this inside your /ETL folder or use docker exec -it instead):

`$ docker-compose run --rm db bash`

Now, inside the db service, access the created database:

And the password being: testpass

`$ psql --host=db --username=henrivis --dbname=rainbow_database`

Inside the database we can give some commands, such:
List all tables:

`$ \d`

Create a new table inside the db:

`$ CREATE TABLE color_table(name TEXT);`

List everything inside a table:

`$ SELECT * FROM color_table;`

Add something to the table:

`$ INSERT INTO color_table VALUES ('red');`

`$ INSERT INTO color_table (name, address, created_at) VALUES ('oi1', 'oi1', now());`

Resources:

- https://medium.com/analytics-vidhya/getting-started-with-postgresql-using-docker-compose-34d6b808c47c


#### When trying to change the .env username and password for the PostgreSQL:

`$ docker volume ls`

Remove the container which is using the volume, in our case is the postgres service, even though is stopped/exited we have to REMOVE the image:

`$ docker rm container_ID`

Now remove the volume:

`$ docker volume rm etl_db-data`

Now, up your services again and the changes should take effect:

`$ docker-compose up`

If you try to Change user's and pwd but the changes don't take effect:
https://github.com/docker-library/postgres/issues/203