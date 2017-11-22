# -*- coding: utf-8 -*-
import config
import telebot
import asyncio
from aiohttp import web
from aiohttp import ClientSession
bot = telebot.AsyncTeleBot(config.token)

# Process webhook calls
async def handle(request):
    print('receive')
    if request.match_info.get('token') == bot.token:
        request_body = await request.json()
        print(request_body)
        await send(request_body['message']['text'])
        return web.Response()
    else:
        return web.Response(status=403)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))

#https://api.themoviedb.org/3/search/movie?api_key=&query=
async def send(text):
    print('send starts', text)
    async with ClientSession() as session:
        params = {'api_key': config.apikey, 'query': text}
        async with session.get('https://api.themoviedb.org/3/search/movie', params=params) as resp:
            text = await resp.text()
            print(text)
if __name__ == '__main__':
	app = web.Application()
	app.router.add_post('/{token}/', handle)
	print('film handler added')
	web.run_app(
    	app,
    	host='0.0.0.0',
    	port=3000,
	)