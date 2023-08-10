
import json
import asyncio
from .mongodb import get_collection
from .utils import timestamp


async def process_log_queue(queue: asyncio.Queue, conn: any, CHANNEL_NAME: str, mode: str, shell_id: int):
    list = []
    sec = 0
    collection = get_collection()
    print("process_log_queue")
    while True:
        data = await queue.get()
        _sec = int(data['timestamp'][-13])
        if sec != _sec and len(list) > 0:
            # 저장
            ret = collection.insert_one({'time': data['timestamp'][:-6], "shell_id": shell_id, 'mode': mode, 'lines': list})
            print(f"insert_to_mongodb: {sec} != {_sec} / {len(list)}: {ret.inserted_id}")
            list = []
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
            "time": timestamp()
        }))
        list.append(data)
        queue.task_done()
