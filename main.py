import asyncio
import datetime
import os
import pandas as pd
# import dropbox
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto

client = TelegramClient('Test', '9324313', 'e5f895ec6fa7c608a62e722a28580f26')
client.start()
# ACCESS_TOKEN = "sl.BZ1T0GMAKomJAKEWwVXDBVMfWLW05_B8w2-77fXPwvwUgKVoDj1g0QW2LieHt_ASAuEP3ne-a8j-RcG9cRkZOndNI4oa_DeWeVFmPIG75VXIienyvTTWZ97wLEG0DE1yUsX8C7Dh"
# dbx = dropbox.Dropbox(ACCESS_TOKEN)

try:
    async def main():
        channel_name = input("Enter channel name: ")
        channel = await client.get_entity(channel_name)
        s_date = input("Enter start date (YYYY-MM-DD): ")
        e_date = input("Enter end date (YYYY-MM-DD): ")
        # s_date = "2023-03-01"
        # e_date = "2023-03-01"
        start_date = datetime.datetime.strptime(s_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(e_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        prefirst_m = await client.get_messages(channel, limit=1, offset_date=start_date)
        first_m = await client.get_messages(channel, min_id=prefirst_m[0].id, limit=1, reverse=True)
        last_m = await client.get_messages(channel, limit=1, offset_date=end_date)
        messages_between = await client.get_messages(channel, min_id=first_m[0].id, max_id=last_m[0].id)
        if messages_between:
            messages_between.insert(0, last_m[0])
            messages_between.append(first_m[0])
        
        if last_m[0].id == first_m[0].id:
            messages_between = last_m

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
                photo_data = await client.download_file(m.media)
                with open(filepath, 'wb') as fd:
                    fd.write(photo_data)
                # dropbox_file_path = f"/{channel.username}/{filename}"
                # with open(filepath, 'rb') as f:
                # dbx.files_upload(photo_data, dropbox_file_path)
                # shared_link = dbx.sharing_create_shared_link(dropbox_file_path)
                # media_info = shared_link.url
                media_info = filepath

            data.append({'channel': channel.username, 'text': m.text, 'id': m.id, 'date': m.date, 'media_info': media_info})
        
        df = pd.DataFrame(data)
        df.dtypes
        df['date'] = df['date'].dt.tz_localize(None)
        end_date = end_date - datetime.timedelta(days=1)
        if s_date == e_date:
            filename = f'{channel.username}_{start_date.date()}.xlsx'
        else:
            filename = f'{channel.username}_{start_date.date()}_{end_date.date()}.xlsx'
        df.to_excel(filename, index=False)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

except:
    print("No data")
