[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Elasticsearch Cluster Monitor

A simple dockerized Django-based Elasticsearch monitor. Have all your clusters at one place and immediately know if any one of them is down.

## Information you get:

1. Is your Elasticsearch Cluster down?
2. Is your Ingest pipeline/logstash working properly?
3. What is the health of the cluster? (Green/Yellow/Red)

## Instructions:

**DO NOT MISS THE FOLLOWING STEPS**
1. Clone the repo
    ``` sh
    $ git clone https://github.com/govind-menon110/django-elasticsearch-monitor-dashboard.git
    ```
2. Configure the env variables
    ``` sh 
    $ cd django-elasticsearch-monitor-dashboard
    ```

    ``` sh
    $ vi .env
    ```

    ``` python
    SECRET_KEY=5(15ds+i2+%ik6z&!yer+ga9m=e%jcqiz_5wszg)r-z!2--b2d #Change this
    DB_NAME=postgres #Note this
    DB_USER=postgres 
    DB_PASS=postgres
    DB_SERVICE=postgres
    DB_PORT=5432
    SU_NAME=admin #Change this
    SU_PASS=Admin123@ #Change this
    SU_EMAIL=admin@test.com
    ```

    ``` sh
    $ vi .env.db
    ```

    ``` python
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=postgres #Same as DB_Name
    ```

3. Configure the docker-compose file

    ``` sh
    $ vi docker-compose.yml
    ```

    ``` yaml
    version: '3.7'

    services:
    web:
        restart: always
        build:
            context: ./django_es
            dockerfile: Dockerfile
        expose:
        - "8000"
        links:
        - postgres:postgres
        volumes:
        - web-static:/static
        env_file: .env
        command: sh -c "/usr/local/bin/gunicorn django_es.wsgi:application -w 3 -b :8000 && /bin/python manage.py collectstatic --no-input"

    nginx:
        restart: always
        build: ./nginx
        ports:
        - "80:80"
        volumes:
        - web-static:/static
        links:
        - web:web

    postgres: # Must be same as DB_Name
        restart: always
        image: postgres:latest
        ports:
        - "5432:5432"
        env_file:
        - ./.env.db
        volumes:
        - pgdata:/var/lib/postgresql/data/

    volumes:
    web-static:
    pgdata:
    ```

4. Update the [nginx config](./nginx/site-conf.conf) if you need to

5. Fill in details of your elasticsearch cluster (I assume you are still in the root directory of the project)
    ``` sh
    $ vi ./django_es/config.json
    ```

    If for example your elasticsearch cluster has the following properties:
    ``` yaml
    1. Name: My_ES
    2. ES_URL: http://1.1.1.1:9200
    3. Kibana_URL: http://1.1.1.1:5601
    4. Query Index: /logstash-*/_search?pretty or 'x' # Note that the url slug must begin with '/'
    5. Kibana_Filter: URL of Dashboard or 'x'
    6. doc_limit: INTEGER (Baseline of logs that one generally observes for half hour)
    7. ES_DESC: Description of ES
    ```
    The `config.json` would look like the following:

    ``` json
    [
    {
        "id":"1",
        "es_name":"My ES",
        "es_url":"http://1.1.1.1:9200",
        "kibana_url":"http://1.1.1.1:5601",
        "query_index":"/logstash-*/_search?pretty",
        "kibana_filter":"http://1.1.1.1:5601",
        "doc_limit":"1000",
        "es_desc":"This is my ES for testing the ES Monitor application"
    },
    {
        "id":"2",
        "es_name":"YOUR_ES_NAME",
        "es_url":"https://ES_URL",
        "kibana_url":"KIBANA_URL",
        "query_index":"/ES_INDEX-*/_search?pretty",
        "kibana_filter":"DASHBOARD/CUSTOM_SEARCH URL",
        "doc_limit":"0",
        "es_desc":"DESCRIPTION"
    }
    ]
    ```

6. Although not necessary, do customize the dashboad according to your needs through the template files `base.html` and `home.html` located [here](./django_es/check_es/templates/check_es)

## Running the Application:

1. Install Docker and Docker-compose according to your system
    ``` sh
    $ sudo apt install docker docker-compose -y
    ```

    OR

    ``` sh
    $ sudo yum install docker docker-compose -y
    ```
2. Start docker daemon
    ``` sh
    $ systemctl start docker
    ```
3. Run docker-compose
    ``` sh
    $ sudo `which docker-compose` up -d
    ```
    1. On some systems there may be a `this version of docker-compose unsupported` error. Please refer to [this](https://github.com/10up/wp-local-docker/issues/58#issuecomment-476786006) document for the same
    2. Some systems may face a permission denied error in docker which is why sudo is added. Reference [this](https://stackoverflow.com/questions/60025430/docker-error-ioerror-errno-13-permission-denied-docker-compose-yml) discussion to solve the same

4. Migrate the database
    ``` sh
    $ sudo `which docker-compose` run -d web python manage.py migrate
    ```

5. Wait for 120s (> 2mins) or so

Your dashboard would be ready!

## Change config after deployment:

If you wish to add/remove Elasticsearch clusters or change anything in the `config.json` file or in the template files, then, after updating the same in the folder on host system, run the following to reflect the changes in docker as well:
``` sh
$ sudo `which docker-compose` up -d --build --force-recreate
```

## References:


1. [Dockerizing Django](https://github.com/realpython/dockerizing-django) Blog Post 1
2. [Dockerizing Django](https://pawamoy.github.io/posts/docker-compose-django-postgres-nginx/) Blog Post 2
3. [Dockerizing Django](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/) Blog Post 3 and its github [repo](https://github.com/testdrivenio/django-on-docker/tree/master/app)
4. [Dockerizing Django](https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial) Blog Post 4
2. [Rebuilding Docker container after config change](https://stackoverflow.com/questions/36884991/how-to-rebuild-docker-container-in-docker-compose-yml)
3. [Performing Migrations in Django Docker container](https://stackoverflow.com/questions/33992867/how-do-you-perform-django-database-migrations-when-using-docker-compose)
4. [Creating a default superuser in Django Docker container](https://stackoverflow.com/questions/30027203/)create-django-super-user-in-a-docker-container-without-inputting-password
5. [Clean Restart of Docker Containers](https://docs.tibco.com/pub/mash-local/4.1.1/doc/html/docker/GUID-BD850566-5B79-4915-987E-430FC38DAAE4.html)
7. [Executing multiple commands in docker-compose](https://stackoverflow.com/questions/30063907/using-docker-compose-how-to-execute-multiple-commands)


