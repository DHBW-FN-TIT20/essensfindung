# Essensfindung
Student project for DHBW-Friedrichshafen to search for restaurant or recipe suggestions.

# Usage
To run the application install the requirements:
```console
pip install requirements.txt
```
OR
```console
poetry install --no-dev
```
You also need the configuration files in the `configuration` Folder.<br>
Just copy the examples in the Folder and fill in the Data.
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
If you use git on console the pre-commit will take affect automatically. This will format the code to reduce merge conflicts and ensure some type of standards.<br>
If you want to manuall start the pre-commit check run:
```console
pre-commit run --all-files
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
pip install -r requirements_dev.txt
```
Here you have to manuel manage the requirements.txt files. Use a fixed versions only.