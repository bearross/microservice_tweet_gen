from typing import Optional, Awaitable
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from sqlalchemy import select, and_
from models.api_keys import APIKeys
from serializers.serializer import Serializer
from settings import datetime_format


class ListHandlers(SessionMixin, RequestHandler):
    """
    List Key handler
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        account_id = self.get_body_argument("account_id")
        serializer = Serializer(account_id=account_id)

        response = {}
        if serializer.validate():
            with self.make_session() as session:
                try:
                    result = session.execute(select(APIKeys).where(
                        and_(APIKeys.account_id == account_id, APIKeys.status == 0))
                    )
                    key_list = []
                    for api_key in result.all():
                        api_key = api_key[0]
                        key_list.append({
                            "owner": str(api_key.account_id),
                            "public_key": str(api_key.id),
                            "secret": api_key.secret,
                            "name": api_key.name,
                            "status": api_key.status,
                            "created_at": api_key.created_at.strftime(datetime_format),
                            "modified_at": api_key.modified_at.strftime(datetime_format)
                        })
                    response["data"] = key_list
                except TypeError:
                    response["errors"] = {"key": ["Not found"]}
        else:
            response["errors"] = serializer.errors

        self.finish(response)
