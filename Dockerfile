# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#Create and activate new env.
RUN python3 -m venv venv
RUN . venv/bin/activate

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

#Download ml100k files from the URL

RUN apt-get update -y && \ 
    apt-get install -y wget &&\
    apt-get install unzip

RUN wget https://files.grouplens.org/datasets/movielens/ml-100k.zip && unzip ml-100k.zip 
RUN mkdir target && rm -rf ml-100k.zip
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

#Run tests
RUN python -m unittest test_etl.py -v

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "main_etl.py"]
