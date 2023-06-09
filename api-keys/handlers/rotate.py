from typing import Optional, Awaitable
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from sqlalchemy import update, text
from models.api_keys import APIKeys, generate_secret
from serializers.serializer import Serializer
import uuid


class RotateKeyHandlers(SessionMixin, RequestHandler):
    """
    Rotate Key handler
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        key_id = self.get_body_argument("key")
        account_id = self.get_body_argument("account_id")
        serializer = Serializer(key_id=key_id, account_id=account_id)

        response = {}
        if serializer.validate():
            with self.make_session() as session:
                try:
                    result = session.execute(update(APIKeys).values(id=uuid.uuid4()).where(APIKeys.id == key_id).returning(text("id")))
                    result = result.fetchone()[0]
                    response["data"] = {"account_id": str(account_id), "key": str(result)}
                except TypeError:
                    response["errors"] = {"key": ["Invalid key"]}
        else:
            response["errors"] = serializer.errors

        self.finish(response)


class RotateSecretHandlers(SessionMixin, RequestHandler):
    """
    Rotate secret handler
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        key_id = self.get_body_argument("key")
        account_id = self.get_body_argument("account_id")
        serializer = Serializer(key_id=key_id, account_id=account_id)

        response = {}
        if serializer.validate():
            with self.make_session() as session:
                try:
                    result = session.execute(update(APIKeys).values(secret=generate_secret()).where(APIKeys.id == key_id).returning(text("secret")))
                    result = result.fetchone()[0]
                    response["data"] = {"owner": str(account_id), "public_key": key_id, "secret": str(result)}
                except TypeError:
                    response["errors"] = {"key": ["Invalid key"]}
        else:
            response["errors"] = serializer.errors

        self.finish(response)
