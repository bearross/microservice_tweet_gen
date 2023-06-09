from typing import Optional, Awaitable
from tornado_sqlalchemy import SessionMixin
from models.api_keys import APIKeys
from middlewares.middleware import MiddlewareHandler
from middlewares.api_key import APIKeyAuthentication
from settings import datetime_format


class DetailHandlers(SessionMixin, MiddlewareHandler):
    """
    Get Detail handler
    """
    api_key_authentication = APIKeyAuthentication

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        response = {}
        with self.make_session() as session:
            result = session.query(APIKeys).filter(APIKeys.id == self.get_api_key()).first()
            response["data"] = dict(
                owner=str(result.account_id),
                public_key=str(result.id),
                secret=result.secret,
                name=result.name,
                status=result.status,
                created_at=result.created_at.strftime(datetime_format),
                modified_at=result.modified_at.strftime(datetime_format)
            )

        self.finish(response)
