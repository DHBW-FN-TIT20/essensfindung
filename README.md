# Essensfindung
Student project for DHBW-Friedrichshafen to search for restaurant or recipe suggestions.<br>
Go to ReadTheDocs: https://dhbw-fn-tit20.github.io/essensfindung/

# Docs
See [GitHub-Pages](https://dhbw-fn-tit20.github.io/essensfindung/)

# Usage
If you want to run it make sure you habe a GoogleAPI KEY<br>
The Application use [Geocoding](https://developers.google.com/maps/documentation/geocoding/requests-geocoding), [place-details](https://developers.google.com/maps/billing-and-pricing/pricing#places-details) and [nearby-search](https://developers.google.com/maps/billing-and-pricing/pricing#nearby-search)<br>
**!!! The GoogleAPI Requests are not for free, so pay attention on the pricing !!!**
## Direct with Python
### Requirements
To run the application install the requirements:
```console
pip install requirements.txt
```
OR
```console
poetry install --no-dev
```

### Configuration
If you **dont** have a PostgreSQL Database use `.env-example1` with only the GOOGLE_API. With this Configuration it will create a SQL-Lite DB in the app folder. Not Recommended for Production!
```console
# Copy the Example
cp .env-example1 .env
# Edit the File
nano .env
```

If you have a PostgreSQL Database use `.env-example2`
```console
# Copy the Example
cp .env-example2 .env
# Edit the File
nano .env
```

#### Impressum / Legal Notice
The legal.json file found at `/static/text/legal.json` should contain information about the hosting entity.
Each property should contains the necessary information with the following format:
 - Full Name (or company name)
 - Address Line 1 (street and house number)
 - Address Line 2 (zip code and city)
 - Phone number (international format)
 - Email (of the contact person)


## Docker
You also can build a docker container
```console
git clone https://github.com/DHBW-FN-TIT20/essensfindung.git
cd essensfindung
docker build essensfindung .
```
If you **dont** have a PostgreSQL Database start the container:
```console
docker run -p 8080:80 \
-v /essensfindung/app/data \
-e GOOGLE_API_KEY=KEY \
-e SECRET_KEY=KEY \
--name essensfindung \
essensfindung
```

If you have a PostgreSQL Database:
```console
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
```

## Docker-Compose
See the `docker-compose.yml` File
# Developing
Python-Verison 3.9 or higher<br>
You can use [pyenv](https://github.com/pyenv/pyenv) to manage you virtual envioremnts.
```console
pyenv install 3.9.7
pyenv rehash
pyenv global 3.9.7
```

Please formatt your Code with [black](https://github.com/psf/black) and validate it with [flake8](https://pypi.org/project/flake8/) and [pylint](https://pypi.org/project/pylint/).

## Pre-Commit
If you use git on console the [pre-commit](https://pre-commit.com) will take affect automatically. This will format the code to reduce merge conflicts and ensure some type of standards.<br>
To activate the automaticall validation type:
```console
pre-commit install
```
If you want to manuall start the pre-commit check run:
```console
pre-commit run
```


## Dependencies
To develop on this project we recommend to use [venv](https://docs.python.org/3/library/venv.html).<br>
You can use some extra tools like:
- [pyenv](https://github.com/pyenv/pyenv) (manage the global python version you can use)
- [pipx](https://github.com/pypa/pipx) (install global packages for all you venv's), 
- [poetry](https://python-poetry.org) (manage the local venv)
### Poetry
To install the requierd dependencies via [poetry](https://python-poetry.org) do:
```console
poetry install
```
To add a **developer** only dependencies do:
```console
poetry add -D [Package] [Package]...
poetry export --dev -f requirements.txt -o requirements-dev.txt
```
To add a **production** dependencies do:
```console
poetry add [Package] [Package]...
poetry export -f requirements.txt -o requirements.txt
```

### pip 
To install the requierd dependencies via pip:
```console
pip install -r requirements-dev.txt
```
Here you have to manuel manage the requirements.txt files. Use a fixed versions only.
