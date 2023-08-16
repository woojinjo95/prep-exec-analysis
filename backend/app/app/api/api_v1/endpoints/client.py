import logging
import os
import asyncio
import redis.asyncio as redis
from app.core.config import settings
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)
router = APIRouter()

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
            var ws = new WebSocket(`ws://${host}:5000/api/v1/client/ws`);
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
CHANNEL_NAME = "command"

@router.get("/test")
async def get():
    return HTMLResponse(html)

@router.websocket('/ws')
async def ws_voting_endpoint(websocket: WebSocket):
    await websocket.accept()
    await redis_connector(websocket)


async def redis_connector(websocket: WebSocket):
    async def consumer_handler(conn: redis, ws: WebSocket):
        try:
            while True:
                message = await ws.receive_text()
                await asyncio.sleep(0.001)
                if message is not None:  # command:로 시작하는 메시지를 control 채널로 발행함
                    await conn.publish(CHANNEL_NAME, message)
        except WebSocketDisconnect as exc:
            logger.error(exc)

    async def producer_handler(pubsub: redis, ws: WebSocket):
        await pubsub.subscribe(CHANNEL_NAME)  # control 채널을 수신함 
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                await asyncio.sleep(0.001)
                if message:
                    await ws.send_text(message.get('data'))
        except Exception as exc:
            logger.error(exc)

    conn = await get_redis_pool()
    pubsub = conn.pubsub()

    consumer_task = consumer_handler(conn=conn, ws=websocket)
    producer_task = producer_handler(pubsub=pubsub, ws=websocket)
    done, pending = await asyncio.wait(
        [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED,
    )
    logger.debug(f"Done task: {done}")
    for task in pending:
        logger.debug(f"Canceling task: {task}")
        task.cancel()


async def get_redis_pool():
    return await redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD, decode_responses=True)
