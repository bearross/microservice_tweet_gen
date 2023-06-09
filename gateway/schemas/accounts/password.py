from graphene import String, Mutation, List
from schemas.json_requests import processed_post
from schemas.base import Errors


class ForgotMutation(Mutation):
    class Arguments:
        username = String()

    reset_request = List(String)
    errors = List(Errors)

    @staticmethod
    def mutate(root, info, **kwargs):
        response = processed_post(
            url="http://cs_account:8001/account/password/forgot",
            data=dict(**kwargs)
        )
        return ForgotMutation(**response)


class ResetMutation(Mutation):
    class Arguments:
        token = String()
        password = String()
        confirm_password = String()

    password_reset = List(String)
    errors = List(Errors)

    @staticmethod
    def mutate(root, info, **kwargs):
        response = processed_post(
            url="http://cs_account:8001/account/password/reset",
            data=dict(**kwargs)
        )
        return ResetMutation(**response)


class UpdateMutation(Mutation):
    class Arguments:
        current_password = String()
        password = String()
        confirm_password = String()

    account = List(String)
    errors = List(Errors)

    @staticmethod
    def mutate(root, info, **kwargs):
        authorization = info.context["request"].headers.get('Authorization')
        headers = {'Authorization': authorization}
        response = processed_post(
            url="http://cs_account:8001/account/password/update",
            data=dict(**kwargs),
            headers=headers
        )
        return UpdateMutation(**response)
