from fastapi import FastAPI
import time
import json
from aio_pika import connect, Message
import aioredis
from model import Calc

redis = aioredis.from_url("redis://localhost")
app = FastAPI()


@app.get("/result")
async def get_result(token:int):
    val_data=await redis.get(token)
    if(val_data!=None):
        return {"token": token,"status":"ok","reuslt":json.loads(val_data)}
    else:
        return {"token": token,"status":"not ready","reuslt":""}
    

@app.post("/calculate")
async def calculate(A:int,B:int):
    token_task=int(time.time())
    json_send={"A":A,"B":A,"token":token_task}
    connection = await connect("amqp://test:test@localhost/")

    channel = await connection.channel()

    await channel.default_exchange.publish(
        Message(json.dumps(json_send).encode("utf-8")),
        routing_key = "calculate"
    )

    await connection.close()
    return {"token": token_task}
#uvicorn ApiService:app --reload