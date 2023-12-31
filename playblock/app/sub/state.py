from sub.db import CHANNEL_NAME
import asyncio
from datetime import datetime
from sub.message import publish_message


async def set_run_state(redis_connection):
    print("run_scenario")
    await redis_connection.hset("testrun", "start_time", datetime.utcnow().timestamp())
    await redis_connection.hset("testrun", "state", "run")
    await redis_connection.publish(CHANNEL_NAME, publish_message("start_playblock_response"))


async def set_analysis_state(redis_connection):
    print("set_analysis_state")
    await redis_connection.hset("testrun", "state", "analysis")
    await redis_connection.publish(CHANNEL_NAME, publish_message("start_analysis_response "))


async def is_run_state(redis_connection):
    state = await redis_connection.hget("testrun", "state") == "run"
    # print(f"scenario = {state}")
    return state


async def is_analysis_state(redis_connection):
    state = await redis_connection.hget("testrun", "state") == "analysis"
    # print(f"analysis = {state}")
    return state


async def set_stop_state(redis_connection, event: asyncio.Event):
    print("stop_scenario")
    event.set()
    await redis_connection.hset("testrun", "state", "stop")
    await redis_connection.hset("testrun", "end_time", datetime.utcnow().timestamp())
    await redis_connection.publish(CHANNEL_NAME, publish_message("stop_playblock_response"))
    await redis_connection.publish(CHANNEL_NAME, publish_message("stop_analysis_response"))


async def set_run_item(redis_connection, block_id: str):
    print(f"set_run_item: {block_id}")
    await redis_connection.hset("testrun", "run_block", block_id)
