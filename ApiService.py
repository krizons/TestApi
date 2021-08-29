from fastapi import FastAPI,Body
import time
import json
import aioredis
from amqp import AMQP 
import random
from model import CalculateRequest,ResultResponse,CalculateResponse
import asyncio

redis = aioredis.from_url("redis://localhost")
app = FastAPI()
MyAqmp=AMQP("amqp://test:test@localhost/")

@app.get("/result",
summary="Получение результата сложения двух переменных",
response_model=ResultResponse,
response_description="Результат сложения двух переменных")
async def get_result(token:int):
    """
    Для получение результата передайте:
    - **token**: Токен для получения результата операции сложения
    """
    # Получаем значение по заданному токену
    val_data=await redis.get(token)
    # Проверяем наличие данных
    if( val_data is not None):
        try:
            #Конвертируем строку в объект
            JsonData=json.loads(val_data)
        except:
            #В случае ошибки конвертации выдает ошибку
            return ResultResponse(token=token,status="fault",reuslt=0) 
        #Проверяем наличие нужного ключа
        if("summ" in JsonData):
            #Всё ок
            return ResultResponse(token=token,status="ok",reuslt=json.loads(val_data)["summ"]) 
        else:
            #Нет ключа
            return ResultResponse(token=token,status="fault",reuslt=0) 
    else:
        #Данные не готовы
        return  ResultResponse(token=token,status="not ready",reuslt=0) 
    

@app.post("/calculate",
summary="Сложение двух переменных",
response_model=CalculateResponse,
response_description="Токен для получения результата",
)
async def calculate(req:CalculateRequest= Body(...)):
    # Генерируем уникальный токен
    token_task=random.randint(0, 1000000) 

    # Помещаем задачу в очередь
    json_send={"A":req.A,"B":req.B,"token":token_task}
    await MyAqmp.publish(
        "calculate",
        json_send
    )
    # Все ОК
    return CalculateResponse(token=token_task)
loop = asyncio.get_event_loop()
loop.create_task(MyAqmp.connect())

#uvicorn ApiService:app --reload