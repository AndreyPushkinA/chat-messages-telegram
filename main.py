import asyncio
import datetime
import os
import pandas as pd
import dropbox
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import MediaEmptyError
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto

client = TelegramClient('Test', '9324313', 'e5f895ec6fa7c608a62e722a28580f26')
client.start()
ACCESS_TOKEN = "sl.BZ006eSK2nzpL97TRLPoz-49KfhzIpWXIe1zofhkHZokORRMy1kmiHkXMZhjf-oPTyjXCItZr_ZtlActhbi3141HWhbaeUizmgvFVKJ4m6k8KZBJ6H8b_pp1Jv8RlJ4CPVmK_uz_"
dbx = dropbox.Dropbox(ACCESS_TOKEN)

async def main():
    channel = await client.get_entity("westernnews24")
    s_date = "2023-03-02"
    e_date = "2023-03-02"
    start_date = datetime.datetime.strptime(s_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(e_date, '%Y-%m-%d') + datetime.timedelta(days=1)
    prefirst_m = await client.get_messages(channel, limit=1, offset_date=start_date)
    first_m = await client.get_messages(channel, min_id=prefirst_m[0].id, limit=1, reverse=True)
    last_m = await client.get_messages(channel, limit=1, offset_date=end_date)
    messages_between = await client.get_messages(channel, min_id=first_m[0].id, max_id=last_m[0].id)
    if messages_between:
        messages_between.insert(0, last_m[0])
        messages_between.append(first_m[0])

    data = []
    if not os.path.exists("media"):
        os.mkdir("media")
    channel_folder = os.path.join('media', channel.username)
    if not os.path.exists(channel_folder):
        os.mkdir(channel_folder)

    for m in messages_between:
        media_info = "None"
        if isinstance(m.media, MessageMediaPhoto):
            filename = f'{channel.username}_photo_{m.id}.jpg'
            filepath = os.path.join(channel_folder, filename)
            with open(filepath, 'wb') as fd:
                photo_data = await client.download_file(m.media)
                fd.write(photo_data)
            dropbox_file_path = f"/{channel.username}/{filename}"
            with open(filepath, 'rb') as f:
                dbx.files_upload(f.read(), dropbox_file_path)
            shared_link = dbx.sharing_create_shared_link(dropbox_file_path)
            media_info = shared_link.url

        data.append({'channel': channel.username, 'text': m.text, 'id': m.id, 'date': m.date, 'media_info': media_info})
        print(m.date)

    df = pd.DataFrame(data)
    df.dtypes
    df['date'] = df['date'].dt.tz_localize(None)
    if s_date == e_date:
        filename = f'{channel.username}_{start_date.date()}.xlsx'
    else:
        filename = f'{channel.username}_{start_date.date()}_{end_date.date()}.xlsx'
    df.to_excel(filename, index=False)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
