build: clean_python
	docker build -t essensfindung .

buildkit: clean_python
	DOCKER_BUILDKIT=1 docker build -t essensfindung .

clean_python:
	find . -type d -name __pycache__ -exec rm -r {} \+
	find . -type d -name .pytest_cache -exec rm -r {} \+
	rm -r -f app/logs
	rm -f app/essensfindung.db
	rm -r -f app/data

clean_docker:
	docker rm --force essensfindung
	docker container prune --force
	docker volume prune --force

clean_all: clean_python clean_python clean_docker
