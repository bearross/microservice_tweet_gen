from unittest import TestCase
from client import client, info


class TestApiKeys(TestCase):
    def test_api_key_detail(self):
        query = """query {
            apiKey{
                detail{
                    owner,
                    publicKey,
                    name,
                    secret,
                    status,
                    createdAt,
                    modifiedAt,
                    errors{
                        key,
                        messages
                    }
                }
            }
        }"""

        variables = {}
        headers = {
            "x-secret-key": "Bearer " + info["secret"],
            "x-api-key": "Bearer " + info["public_key"]
        }
        data = client.execute(query=query, variables=variables, headers=headers)
        _result = {
            'apiKey': {
                'detail': {
                    'owner': info["account_id"],
                    'publicKey': info["public_key"],
                    'name': info["name"],
                    'secret': info["secret"],
                    'status': 0,
                    'createdAt': info["created_at"],
                    'modifiedAt': info["modified_at"],
                    'errors': None
                }
            }
        }

        self.assertDictEqual(data, _result)
