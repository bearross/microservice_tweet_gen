from typing import Optional, Awaitable
from tornado_sqlalchemy import SessionMixin
from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from schemas.schema import schema


class HistoryHandler(SessionMixin, TornadoGraphQLHandler):
    """
    Account handler
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        data = self.parse_body()
        query, variables, operation_name, id = self.get_graphql_params(self.request, data)

        with self.make_session() as session:
            result = schema.execute(query, context_value={'session': session})
            print(result)

        # query, variables, operation_name, id = self.get_graphql_params(self.request, data)
        # try:
        #     document = parse(query)
        #     args = dict()
        #     for member in document.definitions[0].selection_set.selections[0].arguments:
        #         args[member.name.value] = member.value.value
        #     return {
        #         "hi": "hi"
        #     }
        # except:
        #     return self.request

        self.finish({
            "msg": "success"
        })
