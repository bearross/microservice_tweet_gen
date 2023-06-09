from graphene import String, Mutation, List
from schemas.json_requests import processed_post, account_detail
from schemas.base import Errors


class CreateKeyMutation(Mutation):
    class Arguments:
        name = String()

    name = String()
    secret = String()
    public_key = String()
    owner = String()

    errors = List(Errors)

    @staticmethod
    def mutate(root, info, name):
        response = account_detail(info)

        if "account_id" in response.keys():
            account_id = response["account_id"]
            response = processed_post(
                url="http://cs_api_keys:8000/create",
                data=dict(account_id=account_id, name=name)
            )

        return CreateKeyMutation(**response)
