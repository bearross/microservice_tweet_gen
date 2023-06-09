from graphene import String, Mutation, List
from schemas.json_requests import processed_post, account_detail
from schemas.base import Errors


class RotateSecretMutation(Mutation):
    class Arguments:
        public_key = String()

    owner = String()
    public_key = String()
    secret = String()
    errors = List(Errors)

    @staticmethod
    def mutate(root, info, public_key):
        response = account_detail(info)

        if "account_id" in response.keys():
            account_id = response["account_id"]
            response = processed_post(
                url="http://cs_api_keys:8000/secret/rotate",
                data=dict(account_id=account_id, key=public_key)
            )

        return RotateSecretMutation(**response)
