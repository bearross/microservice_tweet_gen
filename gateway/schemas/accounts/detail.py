from graphene import String, ObjectType, Field, Mutation, List
from schemas.json_requests import processed_post, account_detail
from schemas.base import GatewayObjectType, Errors


class AccountInfoNode(GatewayObjectType):
    account_id = String()
    first_name = String()
    last_name = String()
    email = String()
    access_level = String()
    status = String()
    last_login = String()
    joined_on = String()

    class Meta:
        name = "AccountInfoNode"


class SessionAccountNode(ObjectType):
    class Meta:
        name = "SessionAccountNode"

    info = Field(AccountInfoNode)

    def resolve_info(self, info):
        response = account_detail(info)
        return AccountInfoNode(**response)


class AccountUpdateMutation(Mutation):
    class Arguments:
        first_name = String()
        last_name = String()
        email = String()
        username = String()
        password = String()

    account = List(String)
    errors = List(Errors)

    @staticmethod
    def mutate(root, info, **kwargs):
        authorization = info.context["request"].headers.get('Authorization')
        headers = {'Authorization': authorization}
        response = processed_post(
            url="http://cs_account:8001/account/update",
            data=dict(**kwargs),
            headers=headers
        )
        return AccountUpdateMutation(**response)
