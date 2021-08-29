import time
import json
import aioredis
import asyncio
from aio_pika import connect, IncomingMessage

redis = aioredis.from_url("redis://localhost")
async def on_message(message: IncomingMessage):
    json_data=json.loads(message.body)
    if("A" in json_data and "B" in json_data and "token" in json_data):
          await  redis.set(json_data["token"],json.dumps({"summ":json_data["A"]+json_data["B"]}))
async def main(loop):

    connection = await connect(
        "amqp://test:test@localhost/", loop=loop
    )
    channel = await connection.channel()
    queue = await channel.declare_queue("calculate")
    await queue.consume(on_message, no_ack=True)
loop = asyncio.get_event_loop()
loop.create_task(main(loop))
loop.run_forever()