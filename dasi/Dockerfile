# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN apt-get update && apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential && pip install mysqlclient
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# 도커 이미지 경량화
#RUN apk del python3-dev mysqlclient-dev build-base

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dasi.wsgi"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000