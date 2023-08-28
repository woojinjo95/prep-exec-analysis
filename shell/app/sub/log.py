
import json
import asyncio
from .mongodb import get_collection


async def process_log_queue(queue: asyncio.Queue, conn: any, CHANNEL_NAME: str, mode: str, shell_id: int):
    buffer = []
    sec = 0
    collection = get_collection()
    print("process_log_queue")
    while True:
        data = await queue.get()
        _sec = data['timestamp'].second
        if sec != _sec and len(buffer) > 0:
            # 저장
            ret = collection.insert_one(
                {'time': data['timestamp'], "shell_id": shell_id, 'mode': mode, 'lines': buffer})
            print(f"insert_to_mongodb: {sec} != {_sec} / {len(buffer)}: {ret.inserted_id}")
            buffer = []
            sec = _sec
        # print(data)
        await conn.publish(CHANNEL_NAME, json.dumps({
            "msg": "shell",
            "level": "debug",
            "data": {
                "shell_id": shell_id,
                "mode": mode,
                "data": data
            },
            "service": "shell",
            "time": data['timestamp']
        }))
        buffer.append(data)
        queue.task_done()
