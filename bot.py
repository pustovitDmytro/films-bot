# -*- coding: utf-8 -*-
import config
import telebot
from aiohttp import web

async def handler(request):
	print(request.method)
	print(request.scheme)
	return web.Response(text='text')

# async def wshandler(request):
#     ws = web.WebSocketResponse()
#     await ws.prepare(request)

#     async for msg in ws:
#         if msg.type == web.MsgType.text:
#             await ws.send_str("Hello, {}".format(msg.data))
#         elif msg.type == web.MsgType.binary:
#             await ws.send_bytes(msg.data)
#         elif msg.type == web.MsgType.close:
#             break

#     return ws

if __name__ == '__main__':
	app = web.Application()
	app.router.add_get('/films', handler)
	web.run_app(app)