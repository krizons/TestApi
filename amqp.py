from aio_pika import connect, Message
import json
class AMQP:
    URL:str
    
    def __init__(self,url):
      self.URL=url
    async def connect(self):
        self.connection = await connect(self.URL)
        self.channel = await self.connection.channel()
    async def close(self):
        await self.connection.close()  
    async def publish(self,routing_key:str,data:dict):
        await self.channel.default_exchange.publish(
            Message(json.dumps(data).encode("utf-8")),
            routing_key = routing_key
        )    