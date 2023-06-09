from typing import Optional, Awaitable
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from tweet_gen.models.archives import Archive, status_text


class StatusHandler(SessionMixin, RequestHandler):
    """
    Status checking handler for check status of the archive upload.
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self, account, archive_id):
        with self.make_session() as session:
            archive = session.query(Archive).filter(Archive.account_id == account, Archive.id == archive_id).first()
            if archive:
                self.write({
                    "data": {
                        "status": archive.status,
                        "status_text": status_text(archive.status),
                        "archive_id": archive.id,
                        "account_id": str(archive.account_id),
                        "filename": archive.filename
                    },
                })
            else:
                self.write({
                    "errors": {
                        "status": ["Archive not found"]
                    }
                })
