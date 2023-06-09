from typing import Optional, Awaitable
from tornado.web import RequestHandler


class Middleware(object):
    def process_request(self, handler):
        pass

    def process_response(self, handler):
        pass


class MiddlewareHandler(RequestHandler):
    token_authorization = None
    middlewares = []

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get_current_user(self):
        return self.token_authorization.account_id

    def prepare(self):
        self.token_authorization = self.token_authorization()
        self.token_authorization.process_request(self)

        for middleware in self.middlewares:
            middleware = middleware()
            middleware.process_request(self)

    def finish(self, chunk=None):
        super(MiddlewareHandler, self).finish(chunk)

    def write_error(self, status_code, **kwargs):
        exc_cls, exc_instance, trace = kwargs.get("exc_info")
        if status_code != 200:
            self.set_status(status_code)
            self.write({"message": [str(exc_instance)]})
