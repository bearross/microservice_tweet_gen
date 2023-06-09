from typing import Optional, Awaitable

from tornado_sqlalchemy import SessionMixin
from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from schemas.schema import schema
import logging
from tornado.httputil import parse_multipart_form_data


class GraphQLHandler(SessionMixin, TornadoGraphQLHandler):
    """
    Account handler
    """

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        data = self.parse_body()

        query, variables, operation_name, _ = self.get_graphql_params(self.request, data)
        # print(query, variables, operation_name, id)
        with self.make_session() as session:
            result = schema.execute(query, variables=variables, context_value={'session': session, 'request': self.request})

        if result.errors:
            logging.error(result.errors)
            response = {
                "errors": {
                    "input": ["GraphQL input error"]
                }
            }
        else:
            response = result.data

        self.finish(response)
