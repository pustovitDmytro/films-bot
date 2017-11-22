# -*- coding: utf-8 -*-
import config
from aiohttp import web
from aiohttp import ClientSession

# Process webhook calls
async def handle(request):
    print('receive')
    if request.match_info.get('token') == config.token:
        request_body = await request.json()
        films = await getFilm(request_body['message']['text'])
        for film in films:
            await postFilm(film)
        return web.Response()
    else:
        return web.Response(status=403)


async def getFilm(text):
    async with ClientSession() as session:
        params = {'api_key': config.apikey, 'query': text}
        async with session.get('https://api.themoviedb.org/3/search/movie', params=params) as resp:
            body = await resp.json()
            return body['results']

async def postFilm(film):
    data = {}
    data['chat_id'] = 238585617
    data['text'] = film['title']
    await telegram('sendMessage', data)

async def telegram(method, data={}):
    async with ClientSession() as session:
        async with session.post('https://api.telegram.org/bot{}/{}'.format(config.token,method), data=data) as resp:
            return resp.json()
            
if __name__ == '__main__':
	app = web.Application()
	app.router.add_post('/{token}/', handle)
	web.run_app(
    	app,
    	host='0.0.0.0',
    	port=3000,
	)