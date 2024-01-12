![logo.png](logo.png)
# jiushu-logger-starlette【九书 Starlette / FastAPI 路由专用】

## 简介

JF 专用格式化 logger 的 Starlette / FastAPI 路由特供版，专门输出请求日志。

## 使用方法

```python
from asyncio import sleep

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route, Mount

from jiushu_logger_starlette.route_logging_middleware import RouterLoggingMiddleware


async def _test(request: Request):
    # You can get trace id of *this* request.
    # If apache-skywalking is used, this trace_id will be the ID tracing by skywalking.
    return PlainTextResponse(request.state.trace_id.encode('utf_8'))


async def _test2(request: Request):
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
    # Logging for routes.
    # You can set which route should be skipped, 
    #   or which pattern the route matches should be skipped.
    Middleware(RouterLoggingMiddleware,
               skip_routes=['/api/health'],
               skip_regexes=[r'''^.*skip.*$'''])
]
app = Starlette(routes=routes, middleware=middleware)
```
