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

CMD [ "python", "-u", "process.py" ]