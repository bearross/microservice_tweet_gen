import json
import requests
from schemas.base import Errors


def requests_post_json(**kwargs):
    return json.loads(requests.post(**kwargs).text)


def requests_get_json(**kwargs):
    return json.loads(requests.get(**kwargs).text)


def process_response(response):
    _response = {}
    if "data" in response.keys():
        _response = response["data"]

    if "errors" in response.keys():
        errors = []
        for key, messages in response["errors"].items():
            errors.append(Errors(key, messages))
        _response["errors"] = errors

    return _response


def processed_post(**kwargs):
    response = requests_post_json(**kwargs)
    return process_response(response)


def processed_get(**kwargs):
    response = requests_get_json(**kwargs)
    return process_response(response)


def account_detail(info):
    authorization = info.context["request"].headers.get('Authorization')
    headers = {'Authorization': authorization}
    response = processed_post(url="http://cs_account:8001/account/detail", headers=headers)
    return response


def key_detail(info):
    api_key = info.context["request"].headers.get('X-API-KEY')
    secret_key = info.context["request"].headers.get('X-SECRET-KEY')
    headers = {'X-API-KEY': api_key, "X-SECRET-KEY": secret_key}
    response = processed_post(url="http://cs_api_keys:8000/detail", headers=headers)
    return response
