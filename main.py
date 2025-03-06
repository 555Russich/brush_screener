import logging
import re

from telethon import TelegramClient, events

from config import cfg, FILEPATH_LOGGER
from my_logging import get_logger
from enums import UN

client = TelegramClient(cfg.session_filepath, cfg.api_id, cfg.api_hash,  system_version="4.16.30-vxCUSTOM_qwe")


@client.on(events.NewMessage(chats=UN.brush_screener))
async def handle_message_with_urls(event):
    volume_10 = int(re.search(r'(?<=Last 10 mins vol: )\d+', event.raw_text).group(0))
    logging.info('Volume', volume_10)
    if volume_10 >= 9000:
        await client.forward_messages(entity=int(UN.brush_screener_filtered), messages=event.message)


async def main():
    # This part is IMPORTANT, because it fills the entity cache.
    await client.get_dialogs()

    myp = None
    async for dialog in client.iter_dialogs():
        if dialog.name == 'Brush Screener filtered':
            print(dialog.name, dialog.id)
            print(type(dialog.id))
            myp = dialog
            # await client.send_message(entity=int(UN.brush_screener_filtered), message='test')

if __name__ == '__main__':
    get_logger(FILEPATH_LOGGER)

    client.start(phone=cfg.phone, password=cfg.password)
    with client:
        try:
            client.loop.run_until_complete(main())
            client.run_until_disconnected()
        finally:
            logging.info(f'{client.is_connected()=}')
            client.session.save()
