FROM python:3.9.7
ARG DEBIAN_FRONTEND=noninteractive

# install fundamental
RUN apt-get update && apt-get -y install libgl1-mesa-glx x264 libx264-dev libavcodec-dev ffmpeg adb lsof libsqlite3-dev

# install pip & python
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip install --upgrade pip

# install requirements
WORKDIR /app/
ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD . ./

CMD ["python", "main.py"]
