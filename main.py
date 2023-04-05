import json
import asyncio
from helpers import DB
from telethon import TelegramClient, events, types
from telethon.errors import SessionPasswordNeededError
from time import sleep
import logging
logging.basicConfig(level=logging.DEBUG)
with open("config.json", "rb") as file:
    data = json.load(file)
    api_id = data["api_id"]
    api_hash = data["api_hash"]
    phone = data["phone"]
    group_link = data["group_link"]
    TIMEOUT = data["TIMEOUT"]
client = TelegramClient(phone, api_id, api_hash)
db = DB("bot.db")
db.create()


async def message(event):

    sender = await event.get_sender()

    sender_id = sender.id
    """Проверяем, сообщение пришло в группу или в лс"""
    try:
        if type(event.original_update) == types.UpdateNewChannelMessage and not event.sender.bot:
            """если id пользователя не существует в таблице"""
            if not db.is_user_exist(sender_id):
                db.add_user(sender_id)  # Добавляем id пользователя в список
                chat_id = event.chat_id
                message_id = event.message.id
                chat_from = await event.client.get_entity(chat_id)
                message_link = "t.me/" + \
                    chat_from.username + "/" + str(message_id)
                """Пересылаем сообщение в группу"""
                await event.client.send_message(entity=group_link, message=message_link)
                # Ожидаем заданный промежуток времени
                sleep(TIMEOUT)
            # else:
            #     # print(event.original_update)
            #     if type(event.original_update) == types.UpdateNewChannelMessage:
            #         chat_id = event.chat_id
            #         message_id = event.message.id
            #         message_link = "https://t.me/"+str(chat_id)+"/"+str(message_id)
            #         print(event)
            #         # # Пересылаем сообщение в группу
            #         # await event.client.send_message(entity=group_link, message=message_link)
            #         # await asyncio.sleep(TIMEOUT)  # Ожидаем заданный промежуток времени
    except:
        pass


async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone, force_sms=False)
        value = input("Enter login code: ")
        try:
            me = await client.sign_in(phone, code=value)
        except SessionPasswordNeededError:
            password = input("Enter password: ")
            me = await client.sign_in(password=password)
    try:
        client.add_event_handler(message, events.NewMessage)
        await client.run_until_disconnected()
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    asyncio.run(main())
