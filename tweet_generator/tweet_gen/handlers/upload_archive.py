from typing import Optional, Awaitable
from os.path import splitext
from tornado.web import RequestHandler
from tornado import concurrent
import time
from tornado_sqlalchemy import SessionMixin
import datetime

from tweet_gen.utils.parse_twitter_archive import parse_archive
from tweet_gen.utils.collect_texts import collect_texts
from tweet_gen.utils.train import train

executor = concurrent.futures.ThreadPoolExecutor(8)


class UploadArchiveHandler(SessionMixin, RequestHandler):
    """
    Archive uploading handler, runs all tasks in the background and
    return an URL for checking the status of the archive upload.
    Updates status on each task completion so the user can see.

    | Tasks:
    | 1. Uploads Archive
    | 2. Parse necessary content from Twitter Archive
    | 3. Collects required texts
    | 4. Fine-tunes model for the Twitter Archive
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def update_archive_status(self, status):
        with self.make_session() as session:
            session.execute(
                """
                    UPDATE tweet_gen_archives
                    SET status={status}
                    WHERE id={archive_id}
                """.format(archive_id=self.archive_id, status=status)
            )

    def task(self, arg):
        self.update_archive_status(20)
        username = parse_archive(self.account_id, self.filename)

        with self.make_session() as session:
            session.execute(
                """
                    INSERT INTO tweet_gen_usernames(archive_id, username)
                    VALUES ('{archive_id}', '{username}')
                """.format(archive_id=self.archive_id, username=username)
            )

        time.sleep(20)
        self.update_archive_status(21)
        collect_texts(self.account_id)
        self.update_archive_status(22)
        train(self.account_id)
        self.update_archive_status(0)

    def post(self):
        account_id = self.get_body_argument("account_id", default=None, strip=False)

        archive = self.request.files['archive'][0]
        final_filename = str(account_id) + "--" + datetime.datetime.now().strftime("%Y-%m-%d--%H:%M:%S") + ".zip"

        with open("files/archives/" + final_filename, 'wb') as output_file:
            output_file.write(archive['body'])

        data = {
            "account_id": account_id,
            "archive": final_filename
        }

        with self.make_session() as session:
            result = session.execute(
                """
                    INSERT INTO tweet_gen_archives(account_id, filename)
                    VALUES ('{account_id}', '{archive}')
                    RETURNING id
                """.format(**data)
            )
            archive_id = result.fetchone()[0]
            data["archive_id"] = archive_id
            data["status_url"] = "/status/{}/{}/".format(account_id, archive_id)

            self.archive_id = archive_id
            self.account_id = account_id
            self.filename = final_filename
            executor.submit(self.task, datetime.datetime.now())

        self.finish({
            "data": data
        })

