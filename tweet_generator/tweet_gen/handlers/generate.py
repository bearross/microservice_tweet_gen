from typing import Optional, Awaitable
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from tornado import concurrent

from tweet_gen.utils.generate_tweets import generate_tweet

executor = concurrent.futures.ThreadPoolExecutor(8)


class GenerateHandler(SessionMixin, RequestHandler):
    """
    Tweet generation handler using fine-tuned model for each user and
    saves into the database.
    """
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        account_id = self.get_body_argument("account_id", default=None, strip=False)
        url = self.get_body_argument("url", default=None, strip=False)

        with self.make_session() as session:
            result = session.execute(
                """
                    INSERT INTO tweet_gen_urls(account_id, url)
                    VALUES ('{}', '{}')
                    RETURNING id
                """.format(account_id, url)
            )
            url_id = result.fetchone()[0]
        self.account_id = account_id
        self.url = url
        response = {}
        try:
            tweet, text = generate_tweet(self.account_id, self.url)

            with self.make_session() as session:
                result = session.execute(
                    """
                        INSERT INTO tweet_gen_tweets(url_id, account_id, tweet)
                        VALUES ({}, '{}', '{}')
                        RETURNING id
                    """.format(url_id, account_id, url)
                )
                tweet_id = result.fetchone()[0]
                response = {
                    "data": {
                        "account_id": str(account_id),
                        "url_id": url_id,
                        "tweet_id": tweet_id,
                        "url": url,
                        "text": text,
                        "tweet": tweet
                    }
                }
        except IndexError:
            response = {"errors": {
                "tweet_gen": ["No trained file"]
            }}

        self.finish(response)
