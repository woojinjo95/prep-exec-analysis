FROM python:3.11.4-slim-bookworm

WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_DB=0
ENV REDIS_PASSWORD=
ENV CHANNEL_NAME=command
ENV ADB_HOST=192.168.30.25
ENV ADB_PORT=5555
ENV SSH_HOST=192.168.1.23
ENV SSH_USERNAME=nextlab
ENV SSH_PASSWORD=.nextlab1@
ENV SSH_PORT=22
ENV SHELL_TYPE=ssh
ENV MONGODB_USERNAME=admin
ENV MONGODB_PASSWORD=.nextlab6318!
ENV MONGODB_SERVER=mongodb
ENV MONGODB_PORT=27017
ENV MONGODB_NAME=prep-exec-analysis
ENV MONGODB_AUTHENTICATION_SOURCE=admin
ENV MONGODB_COLLECTION_NAME=shell_log

CMD [ "python", "-u", "process.py" ]