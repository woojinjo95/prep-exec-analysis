FROM python:3.9.7
ARG DEBIAN_FRONTEND=noninteractive

# install fundamental
RUN apt-get update
RUN apt-get -y install libsqlite3-dev

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

# CMD ["python", "main.py"]
