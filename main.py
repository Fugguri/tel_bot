from pyrogram import Client
from pyrogram.enums import ChatType
import json
from helpers import DB
from time import sleep
# import logging
# logging.basicConfig(level=logging.DEBUG)
with open("config.json", "rb") as file:
    data = json.load(file)
    api_id = data["api_id"]
    api_hash = data["api_hash"]
    phone = data["phone"]
    group_link = data["group_link"]
    TIMEOUT = data["TIMEOUT"]

db = DB("bot.db")
db.create()

app = Client(phone, api_id, api_hash, phone_number=phone)


@app.on_message()
async def my_handler(client, message):
    sender_id = message.from_user.id
    try:
        if message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP, ChatType.BOT) and not message.from_user.is_bot:
            """если id пользователя не существует в таблице"""
            if not db.is_user_exist(sender_id):
                print(message)
                db.add_user(sender_id)  # Добавляем id пользователя в список
                chat_id = message.chat.id
                message_id = message.id
                chat_from = message.chat.username
                message_link = "t.me/" + \
                    chat_from + "/" + str(message_id)
                """Пересылаем сообщение в группу"""
                await app.send_message(group_link, message_link)
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

try:
    app.run()
except:
    pass
