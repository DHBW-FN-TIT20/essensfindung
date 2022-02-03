# Base Source https://fastapi.tiangolo.com/deployment/docker
FROM python:3.9


# Install Dependencies
COPY ./requirements.txt /tmp/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

# Expose port 80
EXPOSE 80

# Copy the app
RUN mkdir -p /essensfindung/
COPY ./app /essensfindung/app
WORKDIR /essensfindung/app    


# Setup local DB if needed
RUN mkdir data
VOLUME [ "/essensfindung/app/data" ]

# Start gunicorn server with 2 workers, uvicorn worker type and use the 0.0.0.0 host with port 80
ENTRYPOINT ["gunicorn", "-w", "2",  "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80", "main:app"]
