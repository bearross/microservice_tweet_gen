from typing import Optional, Awaitable
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin


class SeedHandler(SessionMixin, RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        with self.make_session() as session:
            results = session.execute(
                """
                    INSERT INTO accounts(first_name, last_name, email, password) VALUES 
                    ('John', 'Doe', 'john@doe.com', 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86'),
                    ('Jane', 'Doe', 'jane@doe.com', 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86')
                """
            )

        self.finish({
            "data": {
                "message": "Successful"
            }
        })

