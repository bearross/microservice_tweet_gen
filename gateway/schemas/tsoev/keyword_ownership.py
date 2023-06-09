from graphene import String, ObjectType, List, JSONString, Mutation, Int, Field
from schemas.json_requests import requests_post_json, account_detail
from graphene_file_upload.scalars import Upload
from schemas.base import Errors


class KeywordNode(ObjectType):
    json = JSONString()


class KeywordsNode(ObjectType):
    class Meta:
        name = "KeywordsNode"

    keywords = List(KeywordNode)
    errors = List(Errors)

    def resolve_keywords(self, info):
        account = account_detail(info)
        response = {}
        if "account_id" in account.keys():
            data = dict(account_id=account["account_id"])
            response = requests_post_json(url="http://cs_tsoev:8006/key-own-get-db", data=data)

        return [KeywordNode(json=response)]


class UploadKeywordOwnershipCSVMutation(Mutation):
    class Arguments:
        csv_file = Upload()
        EnabledPA = String()

    op_status = String()

    @staticmethod
    def mutate(root, info, csv_file, **kwargs):
        if 'csv_file' in info.context["request"].files.keys():
            csv_file = info.context["request"].files['csv_file'][0]["body"]
        else:
            print("no csv file")

        account = account_detail(info)
        response = {}
        if "account_id" in account.keys():
            data = dict(account_id=account["account_id"], **kwargs)
            response = requests_post_json(url="http://cs_tsoev:8006/key-own-upload-csv", data=data, files={"csv_file": csv_file})
        # response = {"op_status": "ok"}
        return AddKeywordOwnershipMutation(**response)


class AddKeywordOwnershipMutation(Mutation):
    class Arguments:
        Keyword = String()
        URL = String()
        Position = Int()
        Traffic = Int()
        PA = Int()

    op_status = String()

    @staticmethod
    def mutate(root, info, **kwargs):
        account = account_detail(info)
        response = {}
        if "account_id" in account.keys():
            data = dict(account_id=account["account_id"], **kwargs)
            response = requests_post_json(url="http://cs_tsoev:8006/key-own-upload-raw", data=data)

        return AddKeywordOwnershipMutation(**response)


class AddKeywordOwnershipURLMutation(Mutation):
    class Arguments:
        Url = String()

    op_status = String()

    @staticmethod
    def mutate(root, info, **kwargs):
        account = account_detail(info)
        response = {}
        if "account_id" in account.keys():
            data = dict(account_id=account["account_id"], **kwargs)
            response = requests_post_json(url="http://cs_tsoev:8006/key-own-from-url", data=data)
        return AddKeywordOwnershipURLMutation(**response)


class OwnKeywordMutation(Mutation):
    op_status = String()

    @staticmethod
    def mutate(root, info, **kwargs):
        account = account_detail(info)
        response = {}
        if "account_id" in account.keys():
            data = dict(account_id=account["account_id"], **kwargs)
            response = requests_post_json(url="http://cs_tsoev:8006/own-keyword", data=data)
        return OwnKeywordMutation(**response)


class OwnKeywordRefreshMutation(Mutation):
    op_status = String()

    @staticmethod
    def mutate(root, info, **kwargs):
        account = account_detail(info)
        response = {}
        if "account_id" in account.keys():
            data = dict(account_id=account["account_id"], **kwargs)
            response = requests_post_json(url="http://cs_tsoev:8006/key-own-refresh", data=data)
        return OwnKeywordRefreshMutation(**response)


class OwnKeywordRevertMutation(Mutation):
    op_status = String()

    @staticmethod
    def mutate(root, info, **kwargs):
        account = account_detail(info)
        response = {}
        if "account_id" in account.keys():
            data = dict(account_id=account["account_id"], **kwargs)
            response = requests_post_json(url="http://cs_tsoev:8006/key-own-revert", data=data)
        return OwnKeywordRevertMutation(**response)


class OwnKeywordResetMutation(Mutation):
    op_status = String()

    @staticmethod
    def mutate(root, info, **kwargs):
        account = account_detail(info)
        response = {}
        if "account_id" in account.keys():
            data = dict(account_id=account["account_id"], **kwargs)
            response = requests_post_json(url="http://cs_tsoev:8006/key-own-reset-db", data=data)
        return OwnKeywordRevertMutation(**response)
