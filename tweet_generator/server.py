from tornado.options import define, options
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import LogFormatter
import logging
from tornado.options import parse_command_line

from tweet_gen.handlers.index import IndexHandler
from tweet_gen.handlers.upload_archive import UploadArchiveHandler
from tweet_gen.handlers.seed import SeedHandler
from tweet_gen.handlers.status import StatusHandler
from tweet_gen.handlers.generate import GenerateHandler
from tweet_gen.settings import db

define("port", default=8002, help="run on the given port", type=int)
parse_command_line()


class DevApplication(Application):
    def __init__(self):
        handlers = [
            (r"/tweet-gen", IndexHandler),
            (r"/tweet-gen/archive/upload", UploadArchiveHandler),
            (r"/tweet-gen/seed", SeedHandler),
            (r"/tweet-gen/status/([a-zA-Z0-9_.-]+)/(\d+)", StatusHandler),
            (r"/tweet-gen/generate", GenerateHandler)
        ]
        Application.__init__(self, handlers, db=db, debug=True)

        formatter = LogFormatter(
            '%(asctime)s.%(msecs)d '
            '%(module)s:%(lineno)d %(levelname)1.1s %(message)s',
            "%Y-%m-%d %H:%M:%S"
        )
        for handler in logging.getLogger().handlers:
            handler.setFormatter(formatter)


def main():
    http_server = HTTPServer(DevApplication())
    http_server.listen(options.port)
    logging.info("Listening to: http://localhost:8002/tweet-gen")
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
