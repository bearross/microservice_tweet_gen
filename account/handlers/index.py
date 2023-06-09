from typing import Optional, Awaitable
from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.write("Welcome to CopyScience Account API.")
