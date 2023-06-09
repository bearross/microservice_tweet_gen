from tornado.options import define, options
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import LogFormatter
import logging
from tornado.options import parse_command_line
import uuid
import base64

from settings import db

from handlers.index import IndexHandler
from handlers.signup import SignupHandler
from handlers.signin import SigninHandler
from handlers.password import UpdateHandler, ResetHandler, ForgotHandler
from handlers.account_detail import AccountDetailHandler
from handlers.account_update import AccountUpdateHandler

define("port", default=8001, help="run on the given port", type=int)
parse_command_line()
index = "account"


class DevApplication(Application):
    def __init__(self):
        handlers = [
            (r"/" + index, IndexHandler),
            (r"/" + index + "/signup", SignupHandler),
            (r"/" + index + "/signin", SigninHandler),
            (r"/" + index + "/password/forgot", ForgotHandler),
            (r"/" + index + "/password/reset", ResetHandler),
            (r"/" + index + "/detail", AccountDetailHandler),
            (r"/" + index + "/update", AccountUpdateHandler),
            (r"/" + index + "/password/update", UpdateHandler)
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
    logging.info("Listening to: http://localhost:" + str(options.port) + "/" + index)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
