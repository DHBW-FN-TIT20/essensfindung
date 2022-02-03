# Base Source https://fastapi.tiangolo.com/deployment/docker
# This is the first stage, to create the requirements.txt
FROM python:3.9 as requirements-stage

WORKDIR /tmp
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    cargo \
    && rm -rf /var/lib/apt/lists/*
RUN pip install poetry
COPY ["./pyproject.toml", "./poetry.lock", "/tmp/"]
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Start final stage
FROM python:3.9

# Install Dependencies
COPY --from=requirements-stage /tmp/requirements.txt /tmp/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

# Expose port 80
EXPOSE 80

# Copy the app
RUN ["mkdir", "-p", "/essensfindung/"]
COPY ./app /essensfindung/app
WORKDIR /essensfindung/app    


# Setup local DB if needed
RUN ["mkdir", "data"]
VOLUME [ "/essensfindung/app/data" ]

# Start gunicorn server with 2 workers, uvicorn worker type and use the 0.0.0.0 host with port 80
ENTRYPOINT ["gunicorn", "-w", "2",  "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80", "main:app"]
