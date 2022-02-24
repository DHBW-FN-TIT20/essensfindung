Usage
=====

.. important:: Essensfindung need a **Google Places API** Token!

Google API Token
----------------

Create your own `API Key <https://cloud.google.com/docs/authentication/api-keys>`_ in this key you have to enable the `Google Maps Places API <https://console.cloud.google.com/apis/library/places-backend.googleapis.com>`_ 
If you already have a Google Project you can activate the API `here <https://console.cloud.google.com/apis/library/places-backend.googleapis.com>`_ 

Installation
------------

You can install the dependencies with::

    pip install requirements.txt


.. hint:: You can also use `Poetry <https://python-poetry.org>`_
    Just use the :file:`pyproject.toml` and the :file:`poetry.lock`

Configuration
-------------

.. warning:: If you dont set the DB Settings the app will use a SQL-Lite DB!
    Dont use this in Production!

.env
^^^^

In the :file:`.env` - File you write all the configurations needed.

Required
    +----------------+-----------------------------------------------------------------+
    | GOOGLE_API_KEY | Your personal Key to the `Google Maps API <#google-api-token>`_ |
    +----------------+-----------------------------------------------------------------+
    | SECRET_KEY     | Your secret key that will be used to hash the JWT - Token       |
    +----------------+-----------------------------------------------------------------+

Optional
    +-------------------+-------------------------------+
    | POSTGRES_USER     | User for the Postgres DB      |
    +-------------------+-------------------------------+
    | POSTGRES_PASSWORD | Password for the User         |
    +-------------------+-------------------------------+
    | POSTGRES_SERVER   | FQDN or IP of the DB server   |
    +-------------------+-------------------------------+
    | POSTGRES_DATABASE | Name of the Database          |
    +-------------------+-------------------------------+
    | POSTGRES_PORT     | Port of the DB [Default 5432] |
    +-------------------+-------------------------------+

Start the APP
-------------

Console
^^^^^^^

.. hint:: This will start the app at port 8000

.. warning:: Do not start the App in Production directly with python.
    Use at least uvicorn


You can simple start the App after the `installation <#installation>`_ and `configuration <#configuration>`_ ::

    python .\main.py

To start it with **uvicorn**::

    uvicorn main:app

to start it with **gunicorn**::

    gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --preload main:app main:app


Docker
------

You also can build a docker container::

    git clone https://github.com/DHBW-FN-TIT20/essensfindung.git
    cd essensfindung
    docker build essensfindung .

If you dont have a **PostgreSQL** Database start the container::

    docker run -p 8080:80 \
    -v /essensfindung/app/data \
    -e GOOGLE_API_KEY=KEY \
    -e SECRET_KEY=KEY \
    --name essensfindung \
    essensfindung

If you have a PostgreSQL Database::

    docker run -p 8080:80 \
    -e GOOGLE_API_KEY=KEY \
    -e SECRET_KEY=KEY \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=PASSWORD \
    -e POSTGRES_SERVER=localhost \
    -e POSTGRES_DATABASE=essensfindung \
    -e POSTGRES_PORT=5432 \
    --name essensfindung \
    essensfindung

Docker Compose
--------------

See the example from :file:`docker-compose.yml`
