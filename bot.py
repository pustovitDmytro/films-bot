# -*- coding: utf-8 -*-
import config
from aiohttp import web
from aiohttp import ClientSession
import json

async def handle(request):
    print('receive')
    if request.match_info.get('token') == config.token:
        request_body = await request.json()
        films = await getFilm(request_body['message']['text'])
        for film in films:
            links = await getLinks(film['title'])
            await postFilm(film, links)
        return web.Response(body = json.dumps(links), status=200)
    else:
        return web.Response(status=403)

async def getLinks(query):
    mvstapeCX = 'partner-pub-7100147019647938:5181683182'
    nnmclubCX = 'partner-pub-7768347321290299:4038489206'
    result = {}
    result['mvstape'] = await googleLink(mvstapeCX,query, 3)
    result['nnmclub'] = await googleLink(nnmclubCX,query+' subs original')
    return result

async def googleLink(cx, query, n=5):
    async with ClientSession() as session:
        params = {'key': config.google,'cx':cx, 'q': query}
        print(query)
        async with session.get('https://www.googleapis.com/customsearch/v1', params=params) as resp:
            body = await resp.json()
            result = []
            for i in range(min(n, int(body['queries']['request'][0]['totalResults']))):
                result.append({"title": body['items'][i]['title'], "link": body['items'][i]['link']})
            return result

async def getFilm(text):
    async with ClientSession() as session:
        params = {'api_key': config.apikey, 'query': text}
        async with session.get('https://api.themoviedb.org/3/search/movie', params=params) as resp:
            body = await resp.json()
            return body['results']

async def postFilm(film, links):
    data = {}
    data['chat_id'] = 238585617
    data['text'] = view(film)
    data['parse_mode']='HTML'
    await telegram('sendMessage', data)

async def telegram(method, data={}):
    async with ClientSession() as session:
        async with session.post('https://api.telegram.org/bot{}/{}'.format(config.token,method), data=data) as resp:
            return resp.json()

def view(film):
    return """
    <b>{}</b>
    """.format(film['title'])

if __name__ == '__main__':
	app = web.Application()
	app.router.add_post('/{token}/', handle)
	web.run_app(
    	app,
    	host='0.0.0.0',
    	port=3000,
	)