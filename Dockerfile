# Base Source https://fastapi.tiangolo.com/deployment/docker
FROM python:3.9


# Install Dependencies
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

# Add new user for security
RUN ["useradd", "--create-home", "--shell", "/bin/bash", "appuser"]
USER appuser

# Expose port 80
EXPOSE 80

# Copy the app
COPY ./app /home/appuser/app
WORKDIR /home/appuser/app

# Start gunicorn server with 2 workers, uvicorn worker type and use the 0.0.0.0 host with port 80
ENTRYPOINT ["gunicorn", "-w", "2",  "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80", "main:app"]
