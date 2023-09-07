
import json
import asyncio
from datetime import datetime
from .mongodb import get_collection


async def process_log_queue(queue: asyncio.Queue, conn: any, CHANNEL_NAME: str, mode: str, shell_id: int, testinfo: dict):
    buffer = []
    collection = get_collection()
    print("process_log_queue")
    while True:
        try:
            data = queue.get_nowait()
            await conn.publish(CHANNEL_NAME, json.dumps({
                "msg": "shell",
                "level": "debug",
                "data": {
                    "mode": mode,
                    "data": data
                },
                "service": "shell",
                "timestamp": data['timestamp']
            }))
            buffer.append(data)
            queue.task_done()
            await asyncio.sleep(0.01)
        except asyncio.QueueEmpty:
            if len(buffer) > 0:
                ret = collection.insert_one({
                    'timestamp': datetime.fromtimestamp(buffer[0]['timestamp']),
                    'mode': mode,
                    'lines': buffer,
                    'scenario_id': testinfo['scenario_id'],
                    'testrun_id': testinfo['testrun_id']
                })
                print(f"insert_to_mongodb: {len(buffer)}: {ret.inserted_id}")
                buffer = []
            else:
                await asyncio.sleep(0.1)
        
