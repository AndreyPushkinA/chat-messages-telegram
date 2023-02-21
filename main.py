import asyncio
import datetime
from datetime import time
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.tl import functions, types

client = TelegramClient('Test', '9324313', 'e5f895ec6fa7c608a62e722a28580f26')
client.start()

async def main():
    channel = await client.get_entity('factcheckmm')
    start_date = datetime.datetime(2023, 2, 3)
    end_date = datetime.datetime(2023, 2, 4)
    prefirst_m = await client.get_messages(channel, limit = 1, offset_date = start_date)
    first_m = await client.get_messages(channel, min_id=prefirst_m[0].id, limit=1, reverse=True)
    last_m = await client.get_messages(channel, limit = 1, offset_date = end_date)
    messages_between = await client.get_messages(channel, min_id=first_m[0].id, max_id=last_m[0].id)
    if messages_between:
        messages_between.insert(0, last_m[0])
        messages_between.append(first_m[0])
    # print(first_m[0].date)
    # print(last_m[0].date)
    for m in messages_between:
        print(m.text, m.date, m.id)
        if isinstance(m.media, MessageMediaPhoto):
                with open('photo.jpg', 'wb') as fd:
                    photo = await client.download_file(m.media)
                    fd.write(photo)
    #then if you want to get all the messages text
    # for x in messages:
    #     print(x.date, x.id)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())