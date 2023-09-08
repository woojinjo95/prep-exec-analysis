
import json
import asyncio
from datetime import datetime
from .mongodb import get_collection


async def process_log_queue(queue: asyncio.Queue, conn: any, CHANNEL_NAME: str, mode: str):
    buffer = []
    collection = get_collection()
    print("process_log_queue")
    while True:
        try:
            msg = "shell"
            data = queue.get_nowait()
            # 입력명령의 경우 응답처리 해줌
            if data['module'] == 'stdin':
                msg = "shell_response"
            
            message = {
                "msg": msg,
                "level": "debug",
                "data": {
                    "mode": mode,
                    "data": data
                },
                "service": "shell",
                "timestamp": data['timestamp']
            }
            message_dump = json.dumps(message)
            print(f"process_log_queue => {message_dump}")
            await conn.publish(CHANNEL_NAME, message_dump)
            buffer.append(data)
            queue.task_done()
            await asyncio.sleep(0.01)
        except asyncio.QueueEmpty:
            if len(buffer) > 0:
                scenario_id = await conn.hget('testrun', 'scenario_id')
                testrun_id = await conn.hget('testrun', 'id')
                ret = collection.insert_one({
                    'timestamp': datetime.fromtimestamp(buffer[0]['timestamp']),
                    'mode': mode,
                    'lines': buffer,
                    'scenario_id': scenario_id,
                    'testrun_id': testrun_id
                })
                print(f"insert_to_mongodb: {len(buffer)}: {ret.inserted_id}")
                buffer = []
            await asyncio.sleep(0.1)
        
