from fastapi import FastAPI
import time
import pika
import json
import aioredis
credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',credentials=credentials))
channel = connection.channel() 
channel.queue_declare(queue='calculate') 
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
def calculate(A:int,B:int):
    token_task=int(time.time())
    json_send={"A":A,"B":B,"token":token_task}
    channel.basic_publish(exchange = "", routing_key = "calculate", body =json.dumps(json_send) )
    return {"token": token_task}
#uvicorn ApiService:app --reload