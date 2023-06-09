from typing import Optional, Awaitable
from tornado.web import RequestHandler


class TestHandler(RequestHandler):
    """
    Account handler
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        file_body = self.request.files['file'][0]['body']
        with open("files/test-post.zip", 'wb') as file:
            file.write(file_body)

        self.finish({
            "result": "hi"
        })
