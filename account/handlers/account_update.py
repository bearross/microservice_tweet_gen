from typing import Optional, Awaitable
from tornado_sqlalchemy import SessionMixin
from middlewares.middleware import MiddlewareHandler
from middlewares.token_authorization import TokenAuthorization
from models.accounts import Account
from sqlalchemy.exc import DataError
from sqlalchemy import update
from serializers.accounts import AccountSerializer


class AccountUpdateHandler(SessionMixin, MiddlewareHandler):
    """
    Account update handler

    Attributes:
    ----------
    token_authorization: Provided TokenAuthorization class validates the authorization
    """
    token_authorization = TokenAuthorization

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        first_name = self.get_body_argument("first_name", default=None, strip=False)
        last_name = self.get_body_argument("last_name", default=None, strip=False)
        email = self.get_body_argument("email", default=None, strip=False)
        username = self.get_body_argument("username", default=None, strip=False)
        password = self.get_body_argument("password", default=None, strip=False)
        response = {}

        serializer = AccountSerializer(first_name=first_name, last_name=last_name, email=email, username=username, current_user=self.get_current_user())

        if serializer.validate():
            try:
                with self.make_session() as session:
                    account = session.query(Account).filter(Account.id == self.get_current_user()).first()
                    if account.check_password(password):
                        del serializer.data["current_user"]
                        session.execute(update(Account).values(**serializer.data).where(Account.id == self.get_current_user()))
                        response["data"] = {
                            "account": ["Account update successful"]
                        }
                    else:
                        response["errors"] = {
                            "password": ["Invalid password"]
                        }
            except (AttributeError, DataError):
                response["errors"] = {"account": ["Account not found"]}
        else:
            response["errors"] = serializer.errors

        self.finish(response)
