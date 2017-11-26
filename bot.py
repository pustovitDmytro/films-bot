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
            film['links'] = links
            await postFilm(film, links)
        return web.Response(body = json.dumps(films), status=200)
    else:
        return web.Response(status=403)

async def getLinks(query):
    mvstapeCX = 'partner-pub-7100147019647938:5181683182'
    nnmclubCX = 'partner-pub-7768347321290299:4038489206'
    result = {}
    result['moviestape'] = await googleLink(mvstapeCX,query, 3)
    result['nnmclub'] = await googleLink(nnmclubCX,query+' subs original')
    return result

async def googleLink(cx, query, n=5):
    async with ClientSession() as session:
        params = {'key': config.google,'cx':cx, 'q': query}
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
    data['text'] = view(film)
    print(view(film))
    data['parse_mode']='Markdown'
    await telegram('sendPhoto', {'photo':"https://image.tmdb.org/t/p/w185{}".format(film['poster_path']) })
    send = await telegram('sendMessage', data)
    print(send)

async def telegram(method, data={}):
    async with ClientSession() as session:
        data['chat_id'] = 238585617
        async with session.post('https://api.telegram.org/bot{}/{}'.format(config.token,method), data=data) as resp:
            return await resp.json()

def view(film):
    links = ""
    for engine in film['links']:
        tmp = list(map((lambda x: "[{}]({})".format(x["title"][:20],x["link"])),film['links'][engine]))
        links += "{}\n{}\n".format(engine, " ".join(tmp))
    return """
*{0} ({1})*
_{2}_
```
{3} popularity
{4} vote average ({5} votes)
```
{6}
    """.format(
        film['title'],        
        film['release_date'][:4],
        film['overview'],
        film['popularity'],
        film['vote_average'],
        film['vote_count'],
        links
    )

if __name__ == '__main__':
	app = web.Application()
	app.router.add_post('/{token}/', handle)
	web.run_app(
    	app,
    	host='0.0.0.0',
    	port=3000,
	)