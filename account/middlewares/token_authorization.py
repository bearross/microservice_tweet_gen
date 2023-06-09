from middlewares.middleware import Middleware

from models.accounts import AuthTokens
from sqlalchemy import and_
from sqlalchemy.exc import DataError


class TokenAuthorization(Middleware):
    account_id = None

    def is_login(self, handler):
        try:
            token = handler.request.headers.get('Authorization').split(" ")[1].strip()

            with handler.make_session() as session:
                token = session.query(AuthTokens).filter(and_(AuthTokens.id == token, AuthTokens.status == 0)).first()
                self.account_id = str(token.account_id)
            return True
        except (AttributeError, DataError):
            handler.finish({"errors": {"authorization": ["Authorization failed"]}})

    def process_request(self, handler):
        self.is_login(handler)
