from typing import Optional, Awaitable
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from serializers.accounts import Account, Serializer
from models.accounts import AuthTokens
from sqlalchemy import or_


class SigninHandler(SessionMixin, RequestHandler):
    """
    User Sign In handler
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        username = self.get_body_argument("username", default=None, strip=False)
        password = self.get_body_argument("password", default=None, strip=False)
        response = {}

        login = Serializer(username=username, password=password)
        if login.validate():
            with self.make_session() as session:
                account = session.query(Account).filter(or_(Account.username == username, Account.email == username)).first()

                if account and account.check_password(password):
                    test = session.query(AuthTokens).filter(AuthTokens.account_id == account.id).first()
                    response["data"] = {
                        "account_id": str(account.id),
                        "token": str(test.id)
                    }
                else:
                    response["errors"] = {
                        "non_field": ["Authentication failed"]
                    }
        else:
            response["errors"] = login.errors

        self.finish(response)
