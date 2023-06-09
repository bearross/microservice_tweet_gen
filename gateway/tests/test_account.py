from unittest import TestCase
from client import client, info


class TestAccount(TestCase):
    def test_sign_in(self):
        query = """mutation signInMutation ($username: String, $password: String) {
            signin(username: $username, password: $password){
                token,
                accountId,
                errors{
                    key,
                    messages
                }
            }
        }"""

        variables = {"username": info["username"], "password": info["password"]}
        data = client.execute(query=query, variables=variables)
        _result = {'signin': {'token': info["token"], 'accountId': info["account_id"], 'errors': None}}
        self.assertDictEqual(data, _result)

    def test_account_detail(self):
        query = """query {
            sessionAccount{
                info {
                    accountId,
                    firstName,
                    lastName,
                    email,
                    accessLevel,
                    status,
                    lastLogin,
                    joinedOn
                }
            }
        }"""

        variables = {}
        headers = {"Authorization": "Token "+info["token"]}
        data = client.execute(query=query, variables=variables, headers=headers)
        _result = {'sessionAccount': {'info': {
            'accountId': info["account_id"],
            'firstName': info["first_name"],
            'lastName': info["last_name"],
            'email': info["username"],
            'accessLevel': '0',
            'status': 'Registered',
            'lastLogin': info["last_login"],
            'joinedOn': info["joined_on"]
        }}}
        self.assertDictEqual(data, _result)
