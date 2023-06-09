from unittest import TestCase
from client import client, info


class TestTweetGen(TestCase):
    def test_archive_upload(self):
        query = """query {
            archive{
                status(archiveId: "1"){
                    accountId,
                    statusText,
                    status,
                    filename,
                    errors {
                        key,
                        messages
                    }
                }
            }
        }"""

        variables = {}
        headers = {
            "Authorization": "Token " + info["token"]
        }
        data = client.execute(query=query, variables=variables, headers=headers)
        _result = {'archive': {'status': {
            'accountId': info["account_id"],
            'statusText': 'Active',
            'status': 0,
            'filename': '735cd182-4e74-4970-a593-22381c31d4cf--2021-05-22--11:02:48.zip',
            'errors': None
        }}}
        self.assertDictEqual(data, _result)
