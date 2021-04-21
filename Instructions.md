### GCP on Linux

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