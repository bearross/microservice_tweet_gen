from tornado.options import define, options
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import LogFormatter
import logging
from tornado.options import parse_command_line


from settings import db

from handlers.index import IndexHandler
from handlers.create import CreateKeyHandlers
from handlers.rotate import RotateKeyHandlers, RotateSecretHandlers
from handlers.update import UpdateHandlers
from handlers.delete import DeleteHandlers
from handlers.list import ListHandlers
from handlers.detail import DetailHandlers

define("port", default=8000, help="run on the given port", type=int)
parse_command_line()


class DevApplication(Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/create", CreateKeyHandlers),
            (r"/key/rotate", RotateKeyHandlers),
            (r"/secret/rotate", RotateSecretHandlers),
            (r"/update", UpdateHandlers),
            (r"/delete", DeleteHandlers),
            (r"/list", ListHandlers),
            (r"/detail", DetailHandlers),
        ]
        Application.__init__(
            self,
            handlers,
            db=db,
            debug=True
        )

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
    logging.info("Listening to: http://localhost:" + str(options.port) + "/")
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
