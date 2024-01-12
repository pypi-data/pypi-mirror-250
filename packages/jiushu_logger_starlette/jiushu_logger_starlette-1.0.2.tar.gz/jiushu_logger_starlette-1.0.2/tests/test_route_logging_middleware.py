# coding: utf-8
from asyncio import sleep
from unittest import TestCase

from jiushu_logger import Logger
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.testclient import TestClient

from jiushu_logger_starlette.route_logging_middleware import RouterLoggingMiddleware

g = {}


async def _test(request: Request):
    g['trace_id'] = request.state.trace_id
    return PlainTextResponse(request.state.trace_id.encode('utf_8'))


async def _test2(request: Request):
    await request.body()
    await request.json()
    await sleep(1.23456)
    return JSONResponse({'result': True}, headers={'Content-Type': 'application/json'})


async def _should_be_skip(request: Request):
    return PlainTextResponse(b'Hello, world!')


async def _health(request: Request):
    return JSONResponse({'status': 'UP'}, headers={'Content-Type': 'application/json'})


routes = [
    Mount('/api', routes=[
        Route('/test', _test),
        Route('/test2', _test2, methods=['GET', 'POST']),
        Route('/should-be-skip', _should_be_skip),
        Route('/health', _health),
    ])
]
middleware = [
    Middleware(RouterLoggingMiddleware,
               skip_routes=['/api/health'],
               skip_regexes=[r'''^.*skip.*$'''])
]
app = Starlette(routes=routes, middleware=middleware)


class RouterLoggingMiddlewareTest(TestCase):
    def test_route_logging_middleware(self):
        with self.assertLogs(Logger.req) as captured:
            client = TestClient(app)
            response = client.get('/api/test')
            client.post('/api/test2',
                        json={'b': '2'},
                        params={'a': '1'},
                        headers=[('My-Header', 'My-Value')], )

            self.assertEqual(response.content, g['trace_id'].encode('utf_8'))
            record = captured.records[0]
            self.assertEqual(record.body, "b''")
            self.assertTrue(isinstance(record.duration, int))
            self.assertEqual(record.path, '/api/test')
            self.assertEqual(record.query, '{}')
            self.assertEqual(record.name, 'jf_service_req')

            record = captured.records[1]
            self.assertEqual(record.body, '{"b":"2"}')
            self.assertTrue(isinstance(record.duration, int))
            self.assertEqual(record.path, '/api/test2')
            self.assertEqual(record.query, '{"a":"1"}')

    def test_skip(self):
        with self.assertRaises(AssertionError):
            with self.assertLogs(Logger.req):
                client = TestClient(app)
                client.get('/api/should-be-skip')
                client.get('/api/health')
