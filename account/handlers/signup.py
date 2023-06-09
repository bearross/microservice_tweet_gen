from typing import Optional, Awaitable
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from serializers.accounts import SignupSerializer, Account
from models.accounts import AuthTokens
from sqlalchemy import insert, text


class SignupHandler(SessionMixin, RequestHandler):
    """
    User Sign Up handler
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        first_name = self.get_body_argument("first_name", default=None, strip=False)
        last_name = self.get_body_argument("last_name", default=None, strip=False)
        username = self.get_body_argument("username", default=None, strip=False)
        email = self.get_body_argument("email", default=None, strip=True)
        password = self.get_body_argument("password", default=None, strip=False)
        confirm_password = self.get_body_argument("confirm_password", default=None, strip=False)

        account = SignupSerializer(first_name=first_name, last_name=last_name, username=username, email=email, password=password, confirm_password=confirm_password)

        response = {}
        if account.validate():
            response["data"] = account.data
            with self.make_session() as session:
                account = Account(**account.data)
                account.set_password(password)
                session.add(account)
                account = session.query(Account).filter(Account.username == account.username).first()
                auth = session.execute(insert(AuthTokens).values(account_id=account.id).returning(text("id"))).fetchone()
                response["data"] = {"account_id": str(account.id), "token": str(auth[0])}

                # TODO send email to account email
        else:
            response["errors"] = account.errors

        self.finish(response)
