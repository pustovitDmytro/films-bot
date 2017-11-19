# -*- coding: utf-8 -*-
import config
import telebot
from aiohttp import web
bot = telebot.TeleBot(config.token)

# Process webhook calls
async def handle(request):
    print('receive', bot.token)
    print(request.match_info.get('token'))
    print('status',request.match_info.get('token') == bot.token)
    if request.match_info.get('token') == bot.token:
        print('true')
        request_body_dict = await request.json()
        print(request_body_dict)
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
	app = web.Application()
	app.router.add_post('/{token}/', handle)
	print('film handler added')
	web.run_app(
    	app,
    	host='0.0.0.0',
    	port=3000,
	)