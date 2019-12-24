import telepot
from bot import BotHandler
import requests
import datetime
from commands import commands
import time

token = '1065331036:AAGk2T8CdUuxV9Z3ycZKRMnG_jmqvrJnH-k'

curr_bot = BotHandler(token)


now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        curr_bot.get_updates(new_offset)

        last_update = curr_bot.get_last_update()

        if last_update is None:
            continue

        try:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']
        except Exception:
            continue

        print(last_chat_text)



        t = last_chat_text.split(' ')
        if t[0] in commands:
            curr_bot.send_message(last_chat_id, commands[t[0]](last_chat_id, t))


        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

