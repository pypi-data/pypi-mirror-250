# coding: utf-8
import re
import typing
from itertools import chain
from time import perf_counter

import orjson
from jiushu_logger import Logger, ReqLogExtra, safely_jsonify
from starlette.applications import Starlette
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from ulid import ULID

try:
    import skywalking
    from skywalking.trace.context import get_context
except:
    skywalking = NotImplemented

__all__ = ['RouterLoggingMiddleware']

# Must be lowercase (see request.headers)
ENV_HEADERS = (
    'x-varnish',
    'x-request-start',
    'x-heroku-queue-depth',
    'x-real-ip',
    'x-forwarded-proto',
    'x-forwarded-protocol',
    'x-forwarded-ssl',
    'x-heroku-queue-wait-time',
    'x-forwarded-for',
    'x-heroku-dynos-in-use',
    'x-forwarded-protocol',
    'x-forwarded-port',
    'x-request-id',
    'via',
    'total-route-time',
    'connect-time'
)


def _get_headers(request: Request):
    headers = dict(request.headers)
    for key in ENV_HEADERS:
        if key in headers:
            del headers[key]
    return headers


class RouterLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self,
                 app: Starlette,
                 *,
                 skip_routes: typing.Sequence[str] = None,
                 skip_regexes: typing.Sequence[str] = None):
        self._skip_routes = skip_routes or []
        self._skip_regexes = (
            [re.compile(regex) for regex in skip_regexes]
            if skip_regexes
            else [])

        super().__init__(app)

    def __should_route_be_skipped(self, request_route: str) -> bool:
        return any(chain(
            iter(True for route in self._skip_routes if request_route.startswith(route)),
            iter(True for regex in self._skip_regexes if regex.match(request_route)),
        ))

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Try to get apache-skywalking trace id. If error, use uuid
        trace_id = None
        if skywalking is not NotImplemented:
            try:
                trace_id = str(get_context().segment.segment_id)
            except:
                pass
        trace_id = trace_id or ULID().hex
        request.state.trace_id = trace_id

        # https://github.com/encode/starlette/issues/495
        data = await request.body()
        form = dict(await request.form())
        try:
            json_ = orjson.loads(data)
        except:
            json_ = None

        if json_ is None:
            if form:
                body = form
            else:
                body = data
        else:
            body = json_

        start_time = perf_counter()
        response = await call_next(request)
        duration = perf_counter() - start_time

        # https://github.com/encode/starlette/issues/495
        resp_body = [section async for section in response.__dict__['body_iterator']]
        response.__setattr__('body_iterator', iterate_in_threadpool(iter(resp_body)))

        # response body
        resp = b''.join(resp_body)
        try:
            resp = orjson.loads(resp)
        except:
            pass

        if not self.__should_route_be_skipped(request.url.path):
            Logger.req.info(
                None,
                extra=ReqLogExtra(
                    trace_id=trace_id,
                    duration=duration,
                    method=request.method,
                    path=request.url.path,
                    client_ip=next(iter(request.headers.getlist('X-Forwarded-For')), request.client.host),
                    host=request.url.hostname,
                    headers=safely_jsonify(_get_headers(request)),
                    query=safely_jsonify(dict(request.query_params)),
                    body=safely_jsonify(body),
                    resp=safely_jsonify(resp)))

        response.headers['X-Request-Id'] = trace_id
        return response
