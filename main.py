import os
import traceback
import asyncio
from aiohttp import web, web_request
import json
from khl import Bot, Cert, Message, Channel, EventTypes, Event
from khl.command import Rule


reply_ch = ''


def open_file(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        tmp = json.load(f)
    return tmp

config = open_file('./config/config.json')

if not config['using_ws']:
    print(f"[BOT] using webhook at port {config['webhook_port']}")
    bot = Bot(cert=Cert(token=config['token'],
                        verify_token=config['verify_token'],
                        encrypt_key=config['encrypt_token']),
              port=config['webhook_port'])
else:
    bot = Bot(token=config['token'])
    

@bot.command()
async def test_cmd(msg: Message):
    try:
        print("test msg recv!")
        ch = await bot.client.fetch_public_channel(ch)

        ret = await ch.send("This is a test msg using ch.send")
        print(f"ch.send | msg_id {ret['msg_id']}")

        ret = await bot.client.send(ch, "This is a test msg using bot.client.send")
        print(f"bot.client.send | msg_id {ret['msg_id']}")
    except:
        print(traceback.format_exc())

@bot.command(rules=[Rule.is_bot_mentioned(bot)])
async def bound_ch(msg: Message, ch_id: str, mentioned: str):
    try:
        print("Channel bound request received!")
        ret = await msg.reply(f'{mentioned}! Channel {ch_id} bounded!')
        print(f"msg.reply | msg_id {ret['msg_id']} | ch_id {ch_id}")
    except:
        print(traceback.format_exc())


if __name__ == '__main__':
    bot.run()
