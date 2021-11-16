# Essensfindung
Student project for DHBW-Friedrichshafen to search for restaurant or recipe suggestions.

# Developing
Python-Verison 3.9 or higher<br>
You can use [pyenv](https://github.com/pyenv/pyenv) to manage you virtual envioremnts.
```console
pyenv install 3.9.7
pyenv rehash
pyenv global 3.9.7
```

Please formatt your Code with [black](https://github.com/psf/black) and validate it with [flake8](https://pypi.org/project/flake8/) and [pylint](https://pypi.org/project/pylint/).

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
```
To add a **production** dependencies do:
```console
poetry add [Package] [Package]...
```

### pip 
To install the requierd dependencies via pip:
```console
pip install -r dev_requirements.txt
```
Here you have to manuel manage the requirements.txt files. Use a fixed versions only.