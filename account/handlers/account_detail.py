from typing import Optional, Awaitable
from tornado_sqlalchemy import SessionMixin
from middlewares.middleware import MiddlewareHandler
from middlewares.token_authorization import TokenAuthorization
from models.accounts import Account, status_text
from settings import datetime_format
from sqlalchemy.exc import DataError


class AccountDetailHandler(SessionMixin, MiddlewareHandler):
    """
    Account detail handler takes AuthToken as Authorization header and returns user details

    Attributes:
    ----------
    token_authorization: Provided TokenAuthorization class validates the authorization
    """
    token_authorization = TokenAuthorization

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        response = {}

        try:
            with self.make_session() as session:
                account = session.query(Account).filter(Account.id == self.get_current_user()).first()
                response["data"] = {
                    "account_id": str(account.id),
                    "first_name": account.first_name,
                    "last_name": account.last_name,
                    "email": account.email,
                    "access_level": account.access_level,
                    "status": status_text(account.status),
                    "last_login": account.last_login.strftime(datetime_format),
                    "joined_on": account.joined_on.strftime(datetime_format)
                }
        except (AttributeError, DataError):
            response["errors"] = {"account": ["Account not found"]}
        self.finish(response)
