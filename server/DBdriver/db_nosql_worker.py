import motor.motor_asyncio
import asyncio
import random
import datetime
from loguru import logger

class MongoDBWorker:
    def __init__(self, ip, port):
        client = motor.motor_asyncio.AsyncIOMotorClient(ip, port)
        self.db = client
        logger.info(self.db)


    async def insert_message(self, message_obj):
        result = await self.db[f'channel_{message_obj["channelId"]}']['message_collection'].insert_one(message_obj)
        del message_obj['_id']
        return result.inserted_id

    async def get_message_for_channel(self, channel_id, page = 1, per_page = 20):
        skips = per_page * (page - 1)
        cursor = self.db[f'channel_{channel_id}']['message_collection'].find().skip(skips).limit(per_page).sort('_id', -1)
        messages = []
        async for msg in cursor:
            del msg['_id']
            messages.append(msg)
        return messages

if __name__ == "__main__":
    def get_message():
        return {
            "text": random.randint(20, 120),
            "username": "forevka",
            "avatar": "qwe",
            "userid": 18,
            "channelId": 1,
            "timestamp": datetime.datetime.now()
        }
    loop = asyncio.get_event_loop()
    mongo = MongoDBWorker('localhost', 27017)
    #for i in range(0, 50, 1):
    #    inserted = loop.run_until_complete(mongo.insert_message(get_message()))
    messages_in_channel = loop.run_until_complete(mongo.get_message_for_channel(2, page = 1))
    for i in messages_in_channel:
        print(i)
