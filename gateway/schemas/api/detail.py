from graphene import String, ObjectType, Int, Field, List
from schemas.json_requests import processed_post
from schemas.base import Errors
from schemas.json_requests import account_detail, key_detail


class DetailNode(ObjectType):
    owner = String()
    name = String()
    public_key = String()
    secret = String()
    status = Int()
    created_at = String()
    modified_at = String()
    errors = List(Errors)

    class Meta:
        name = "DetailNode"


class DetailListNode(ObjectType):
    keys = List(DetailNode)
    errors = List(Errors)

    class Meta:
        name = "DetailListNode"


class KeyNode(ObjectType):
    class Meta:
        name = "KeyNode"

    detail = Field(DetailNode)
    list = Field(DetailListNode)

    def resolve_detail(self, info):
        response = key_detail(info)

        return DetailNode(**response)

    def resolve_list(self, info, **kwargs):
        account = account_detail(info)
        r = {}
        if "account_id" in account.keys():
            response = processed_post(url="http://cs_api_keys:8000/list", data={"account_id": account["account_id"]})
            response = [DetailNode(**r) for r in response]
            r = {**r, "keys": response}
        else:
            errors = account["errors"] if "errors" in account.keys() else []
            r = {**r, "errors": errors}

        return DetailListNode(**r)
