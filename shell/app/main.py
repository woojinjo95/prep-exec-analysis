from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
import asyncio
import redis.asyncio as redis
import logging
import logging.config
import os

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", '')
CHANNEL_NAME = os.getenv("CHANNEL_NAME", 'shell')

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var host = window.location.hostname;
            var ws = new WebSocket(`ws://${host}:5005/ws`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/", tags=['websocket'])
def testclient():
    logger.info("testclient task:")
    return HTMLResponse(html)


@app.websocket('/ws')
async def ws_voting_endpoint(websocket: WebSocket):
    logger.info("websocket task:")
    await websocket.accept()
    await connector(websocket)


async def connector(websocket: WebSocket):
    # 임시로 레디스 웹소켓 연결을 구성한다.
    # 웹소켓 연결여부와 상관없이 레디스 소켓 구성은 되어야 함
    async def consumer_handler(conn: redis, ws: WebSocket):
        try:
            while True:
                message = await ws.receive_text()
                if message is not None:  # command:로 시작하는 메시지를 control 채널로 발행함
                    await conn.publish(CHANNEL_NAME, message)
        except WebSocketDisconnect as exc:
            logger.error(exc)
        except Exception as exc:
            logger.error(exc)

    async def producer_handler(pubsub: redis, ws: WebSocket):
        await pubsub.subscribe(CHANNEL_NAME)  # control 채널을 수신함
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    await ws.send_text(message.get('data'))
        except Exception as exc:
            logger.error(exc)
    
    conn = await get_redis_pool()
    pubsub = conn.pubsub()

    consumer_task = asyncio.create_task(consumer_handler(conn=conn, ws=websocket))
    producer_task = asyncio.create_task(producer_handler(pubsub=pubsub, ws=websocket))
    done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED)
    logger.debug(f"Done task: {done}")
    for task in pending:
        logger.debug(f"Canceling task: {task}")
        task.cancel()

async def get_redis_pool():
    return await redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)