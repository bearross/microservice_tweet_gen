from typing import Optional, Awaitable
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from sqlalchemy import insert, text
from models.api_keys import APIKeys
from serializers.serializer import Serializer


class CreateKeyHandlers(SessionMixin, RequestHandler):
    """
    Create Key handler
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        name = self.get_body_argument("name")
        account_id = self.get_body_argument("account_id")
        serializer = Serializer(name=name, account_id=account_id)
        response = {}
        if serializer.validate():

            with self.make_session() as session:
                result = session.execute(insert(APIKeys).values(account_id=account_id, name=name).returning(text("id, secret"))).fetchone()

            response["data"] = dict(owner=serializer.data["account_id"], name=name, public_key=str(result[0]), secret=result[1])
        else:
            response["errors"] = serializer.errors

        self.finish(response)
