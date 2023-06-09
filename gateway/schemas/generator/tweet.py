from graphene import String, ObjectType, Int, Field, Mutation, List
from schemas.json_requests import processed_post, processed_get, account_detail
from graphene_file_upload.scalars import Upload
from schemas.base import Errors
import base64
from mimetypes import guess_type, guess_extension


class UploadStatusNode(ObjectType):
    account_id = String()
    status = Int()
    status_text = String()
    archive_id = Int()
    filename = String()
    errors = List(Errors)

    class Meta:
        name = "UploadStatusNode"


class TweetNode(ObjectType):
    account_id = String()
    url_id = Int()
    url = String()
    tweet_id = Int()
    text = String()
    tweet = String()

    class Meta:
        name = "TweetNode"


class GeneratorNode(ObjectType):
    class Meta:
        name = "GeneratorNode"

    tweet = Field(TweetNode, url=String(required=True))

    def resolve_tweet(self, info, url):
        account = account_detail(info)
        response = {}
        if "account_id" in account.keys():
            data = dict(account_id=account["account_id"], url=url)
            response = processed_post(url="http://cs_tweet_gen:8002/tweet-gen/generate", data=data)
        return TweetNode(**response)


class ArchiveUploadStatusNode(ObjectType):
    class Meta:
        name = "ArchiveUploadStatusNode"

    status = Field(UploadStatusNode, archive_id=String(required=True))

    def resolve_status(self, info, archive_id):
        account = account_detail(info)
        response = {}
        if "account_id" in account.keys():
            response = {**response, **processed_get(
                url="http://cs_tweet_gen:8002/tweet-gen/status/{}/{}".format(account["account_id"], archive_id))}

        return UploadStatusNode(**response)


class ArchiveUploadMutation(Mutation):
    class Arguments:
        archive = Upload()

    account_id = String()
    archive_id = Int()
    archive = String()
    status_url = String()
    errors = List(Errors)

    @staticmethod
    def mutate(root, info, archive, **kwargs):
        authorization = info.context["request"].headers.get('Authorization')
        headers = {'Authorization': authorization}
        response = processed_post(
            url="http://cs_account:8001/account/detail",
            data=dict(**kwargs),
            headers=headers
        )
        if 'archive' in info.context["request"].files.keys():
            archive = info.context["request"].files['archive'][0]["body"]
        else:
            archive = archive.split(",")
            archive[0] = archive[0] + ","
            file_type = guess_extension(guess_type(archive[0])[0])
            archive = base64.b64decode(archive[1])

        if "account_id" in response.keys():
            account_id = response["account_id"]
            response = processed_post(
                url="http://cs_tweet_gen:8002/tweet-gen/archive/upload",
                data=dict(account_id=account_id),
                files={"archive": archive}
            )

        return ArchiveUploadMutation(**response)
