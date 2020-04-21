import string, random, asyncio
from aiohttp.web import (Response, StreamResponse, RouteTableDef,
                         Application, run_app, HTTPTemporaryRedirect)

routes = RouteTableDef()
char_qty = 10000

# Manager Redirection endpoints
@routes.get('/first_endpoint', name='first_endpoint')
async def first_endpoint(request):
    location = request.app.router['second_endpoint'].url_for()
    raise HTTPTemporaryRedirect(location=location)


@routes.get('/second_endpoint', name='second_endpoint')
async def second_endpoint(request):
    location = request.app.router['final_endpoint'].url_for()
    raise HTTPTemporaryRedirect(location=location)


@routes.get('/final_endpoint', name='final_endpoint')
async def final_endpoint(request):
    response = StreamResponse(
        status=200,
        reason='OK',
        headers={'Content-Type': 'text/plain', 'Content-Length': f'{char_qty}'}
    )
    await response.prepare(request)
    await _write_resp(response)
    response.force_close()
    return response

# Cyclic Endpoints
@routes.get('/first_cyclic_endpoint', name='first_cyclic_endpoint')
async def first_cyclic_endpoint(request):
    location = request.app.router['second_cyclic_endpoint'].url_for()
    raise HTTPTemporaryRedirect(location=location)


@routes.get('/second_cyclic_endpoint', name='second_cyclic_endpoint')
async def second_cyclic_endpoint(request):
    location = request.app.router['first_cyclic_endpoint'].url_for()
    raise HTTPTemporaryRedirect(location=location)


async def _write_resp(response):
    async for line in _gen_rnd_data():
        await response.write(line.encode('utf-8'))
    await response.write_eof()


async def _gen_rnd_data(chunk_size=1):
    letters = string.ascii_lowercase
    ind = 1
    while ind < char_qty:
        yield ''.join(random.choice(letters) for i in range(chunk_size))
        ind += 1


if __name__ == '__main__':
    app = Application(debug=True)
    app.add_routes(routes)
    run_app(app, port=9005)





