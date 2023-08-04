FROM python:3.9.7
ARG DEBIAN_FRONTEND=noninteractive

# install fundamental
RUN apt-get update
RUN apt-get -y install libsqlite3-dev adb

# install pip & python
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip install --upgrade pip

# install requirements
WORKDIR /app/
ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD . ./

ENV MONGODB_SERVER mongodb
ENV MONGODB_NAME prep-exec-analysis
ENV MONGODB_PORT 27017
ENV MONGODB_USERNAME admin
ENV MONGODB_PASSWORD .nextlab6318!
ENV MONGODB_AUTHENTICATION_SOURCE admin
# mongodb://admin:.nextlab6318!@127.0.0.1:27017/prep-exec-analysis?authSource=admin&readPreference=primary&ssl=false

ENV REDIS_HOST redis
ENV REDIS_PORT 6379
ENV REDIS_DB 0
ENV REDIS_PASSWORD 66b44dcb7f981904f8536b19e4464725

ENV DUMP_TIME_LIMIT=60

# CMD ["python", "main.py"]
