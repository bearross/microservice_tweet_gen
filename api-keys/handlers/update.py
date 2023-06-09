from typing import Optional, Awaitable
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from sqlalchemy import update
from models.api_keys import APIKeys
from serializers.serializer import Serializer


class UpdateHandlers(SessionMixin, RequestHandler):
    """
    Update Key Name handler
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        key_id = self.get_body_argument("key")
        name = self.get_body_argument("name")
        account_id = self.get_body_argument("account_id")
        serializer = Serializer(key_id=key_id, name=name, account_id=account_id)

        response = {}
        if serializer.validate():
            with self.make_session() as session:
                try:
                    result = session.execute(update(APIKeys).values(name=name).where(APIKeys.id == key_id))
                    if result.rowcount > 0:
                        response["data"] = {"name": ["Name updated"]}
                    else:
                        raise TypeError("Not found")
                except TypeError:
                    response["errors"] = {"key": ["Invalid key"]}
        else:
            response["errors"] = serializer.errors

        self.finish(response)
