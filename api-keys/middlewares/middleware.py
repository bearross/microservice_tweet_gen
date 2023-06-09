from typing import Optional, Awaitable
from tornado.web import RequestHandler


class Middleware(object):
    def process_request(self, handler):
        pass

    def process_response(self, handler):
        pass


class MiddlewareHandler(RequestHandler):
    api_key_authentication = None

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get_api_key_owner(self):
        return self.api_key_authentication.account_id

    def get_api_key(self):
        return self.api_key_authentication.public_key

    def prepare(self):
        self.api_key_authentication = self.api_key_authentication()
        self.api_key_authentication.process_request(self)

    def finish(self, chunk=None):
        super(MiddlewareHandler, self).finish(chunk)

    def write_error(self, status_code, **kwargs):
        exc_cls, exc_instance, trace = kwargs.get("exc_info")
        if status_code != 200:
            self.set_status(status_code)
            self.write({"massage": [str(exc_instance)]})
