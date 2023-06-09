from middlewares.middleware import Middleware
from models.api_keys import APIKeys
from sqlalchemy import and_
from sqlalchemy.exc import DataError


class APIKeyAuthentication(Middleware):
    account_id = None
    name = None
    public_key = None

    def authenticated(self, handler):
        try:
            public_key = handler.request.headers.get('X-API-KEY').split(" ")[1].strip()
            secret = handler.request.headers.get('X-SECRET-KEY').split(" ")[1].strip()

            with handler.make_session() as session:
                key = session.query(APIKeys).filter(and_(APIKeys.id == public_key, APIKeys.secret == secret, APIKeys.status == 0)).first()
                self.account_id = str(key.account_id)
                self.name = key.name
                self.public_key = key.id
            return True
        except (AttributeError, DataError) as e:
            handler.finish({"errors": {"api_key": ["API key authorization failed"]}})

    def process_request(self, handler):
        self.authenticated(handler)
