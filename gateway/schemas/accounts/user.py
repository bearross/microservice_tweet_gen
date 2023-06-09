from graphene import String, Mutation, List
from schemas.json_requests import processed_post
from schemas.base import Errors


class SignUpMutation(Mutation):
    class Arguments:
        first_name = String()
        last_name = String()
        email = String()
        username = String()
        password = String()
        confirm_password = String()

    account_id = String()
    token = String()
    errors = List(Errors)

    @staticmethod
    def mutate(root, info, **kwargs):
        response = processed_post(
            url="http://cs_account:8001/account/signup",
            data=dict(**kwargs)
        )
        return SignUpMutation(**response)


class SignInMutation(Mutation):
    class Arguments:
        username = String()
        password = String()

    account_id = String()
    token = String()
    errors = List(Errors)

    @staticmethod
    def mutate(root, info, **kwargs):
        response = processed_post(
            url="http://cs_account:8001/account/signin",
            data=dict(**kwargs)
        )
        return SignInMutation(**response)
