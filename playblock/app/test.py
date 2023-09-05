import logging
import os
import time
import json
import shutil
import pika
from datetime import datetime
import sentry_sdk
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
sentry_sdk.init("https://c80f80b497df4c5a9a5fc501486ff9ef@o368530.ingest.sentry.io/5192960")

script_path = os.path.dirname(os.path.realpath(__file__))

# Gets or creates a logger
logger = logging.getLogger(__name__)

# set log level
logger.setLevel(logging.INFO)

# define file handler and set formatter
if not os.path.isdir(os.path.join(script_path, "log")):
    os.mkdir(os.path.join(script_path, "log"))
file_handler = TimedRotatingFileHandler(os.path.join(script_path, "log", "watchdog.log"), when="midnight", interval=1)
logFormat = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
formatter = logging.Formatter(logFormat, datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())


class XrayImageCreated(FileSystemEventHandler):
    def __init__(self):
        self.pre_created_imgbyte = None
        self.pre_created_name = None
        with open(os.path.join(script_path, 'config.json')) as config_file:
            self.config = json.load(config_file)
            logger.info(self.config)
        while True:
            try:
                self.connect()
                break
            except Exception as e:
                logger.error(e)
                time.sleep(3)

    def connect(self):
        self.disconnect()
        try:
            logger.info("Try..Connect: ")
            if self.config["remote"]:
                self.credentials = pika.PlainCredentials(
                    self.config["id"], self.config["pw"])
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        blocked_connection_timeout=3,
                        host=self.config["host"],
                        credentials=self.credentials,))
            else:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        blocked_connection_timeout=3,
                        host='localhost'))
            self.channel = self.connection.channel()
            logger.info(" connected:  ")
        except Exception as e:
            logger.error(e)

    def disconnect(self):
        try:
            self.channel.close()
            self.channel = None
        except Exception as e:
            logger.info(e)
        try:
            self.connection.close()
            self.connection = None
        except Exception as e:
            logger.info(e)

    def on_created(self, event):
        _, ext = os.path.splitext(event.src_path)
        ext = ext.lower()
        basename = os.path.basename(event.src_path)
        # 파일명 또는 확장자 해당 없으면 리턴
        if "-orig" not in basename:
            return

        # 해당 파일이 여전히 수정 불가능인 경우(쓰기 중이면) 리턴
        try:
            Path(event.src_path).touch()
        except Exception as e:
            logger.info(e)
            return

        # 해당 파일을 읽는 과정에서 파일 이동등으로 에러가 날 경우 리턴
        try:
            with open(event.src_path, "rb") as fp:
                srcBytes = fp.read()
        except Exception as e:
            logger.info(e)
            return

        # logger.info("Try..: " + basename)

        mtime = os.path.getmtime(event.src_path)
        creationTime = datetime.fromtimestamp(mtime)

        # Convert ext to bytearray
        ext = bytearray(ext + "/", 'utf8')

        # 해당 파일 읽어서 바로 전송함.
        for _ in range(10):
            try:
                # 이전 이미지와 동일한 이미지가 들어올 경우 return
                if self.pre_created_imgbyte == srcBytes:
                    logger.info("same bytes")
                    return
                if self.pre_created_name == event.src_path:
                    logger.info("same name")
                    return
                timeStr = creationTime.strftime("%Y%m%d, %H:%M:%S:%f")
                timeBArr = bytearray(timeStr, 'utf8')
                messageBArr = ext + timeBArr + srcBytes
                self.channel.basic_publish(
                    exchange='',
                    routing_key="analysis_queue",
                    body=messageBArr)
                logger.info(" [x] Sent 'publish_time' " + timeStr)
                # publish 성공할 경우 이전 이미지 업데이트
                self.pre_created_imgbyte = srcBytes
                self.pre_created_name = event.src_path
                break
            except Exception as e:
                logger.error(e)
                self.connect()
        tid = creationTime.strftime("%Y%m%d%H%M%S%f")
        logger.info(" [x] Sent 'Report' TimeID: {}  FileName: {} CreationTime: {}".format(tid, basename, creationTime.timestamp() * 1000))
        time.sleep(0.05)

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()


if __name__ == "__main__":
    xray_instance = XrayImageCreated()
    observer = Observer()
    observer.schedule(
        xray_instance,
        xray_instance.config["target"],
        recursive=True)
    observer.start()
    logger.info("watchdog start")
    try:
        while True:
            time.sleep(10)
        observer.stop()
    except KeyboardInterrupt:
        observer.stop()
    logger.info("watchdog end")
    observer.join()
