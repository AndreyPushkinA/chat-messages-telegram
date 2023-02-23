import asyncio
import csv
import os
import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.tl.types import DocumentAttributeFilename
from telethon.errors.rpcerrorlist import MediaEmptyError

client = TelegramClient('Test', '9324313', 'e5f895ec6fa7c608a62e722a28580f26')
client.start()

async def main():
    channel = await client.get_entity('factcheckmm')
    start_date = datetime.datetime(2023, 2, 23)
    end_date = datetime.datetime(2023, 2, 24)
    prefirst_m = await client.get_messages(channel, limit=1, offset_date=start_date)
    first_m = await client.get_messages(channel, min_id=prefirst_m[0].id, limit=1, reverse=True)
    last_m = await client.get_messages(channel, limit=1, offset_date=end_date)
    messages_between = await client.get_messages(channel, min_id=first_m[0].id, max_id=last_m[0].id)

    with open(f'{channel.username}_messages_{start_date.date()}_{end_date.date()}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['channel_name', 'text', 'message_id', 'message_date', 'media'])

        if not os.path.exists("media"):
            os.mkdir("media")
        channel_folder = os.path.join('media', channel.username)
        if not os.path.exists(channel_folder):
            os.mkdir(channel_folder)

        for m in messages_between:
            if isinstance(m.media, MessageMediaPhoto):
                filename = f'{channel.username}_photo_{m.id}.jpg'
                filepath = os.path.join(channel_folder, filename)
                with open(filepath, 'wb') as fd:
                    photo_data = await client.download_file(m.media)
                    fd.write(photo_data)
                media_info = filepath

            writer.writerow([channel.username, m.text, m.id, m.date, media_info])

            print(m.text, m.date, m.id, media_info)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
