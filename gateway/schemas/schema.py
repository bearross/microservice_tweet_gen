from graphene import List, ObjectType, Field, Schema
from schemas.accounts.password import ResetMutation, ForgotMutation, UpdateMutation
from schemas.accounts.user import SignInMutation, SignUpMutation
from schemas.accounts.detail import SessionAccountNode, AccountUpdateMutation
from schemas.dummies import History, Person, CreatePerson, UploadFile
from schemas.generator.tweet import GeneratorNode, ArchiveUploadStatusNode, ArchiveUploadMutation
from schemas.api.detail import KeyNode
from schemas.api.rorate import RotateSecretMutation
from schemas.api.update import UpdateKeyMutation
from schemas.api.delete import DeleteKeyMutation
from schemas.api.create import CreateKeyMutation
from schemas.tsoev.keyword_ownership import KeywordsNode, AddKeywordOwnershipMutation, AddKeywordOwnershipURLMutation
from schemas.tsoev.keyword_ownership import OwnKeywordMutation, OwnKeywordRefreshMutation, OwnKeywordRevertMutation
from schemas.tsoev.keyword_ownership import OwnKeywordResetMutation, UploadKeywordOwnershipCSVMutation


class Query(ObjectType):
    history = List(History)
    session_account = Field(SessionAccountNode)
    person = Field(Person)
    generator = Field(GeneratorNode)
    archive = Field(ArchiveUploadStatusNode)
    api_key = Field(KeyNode)
    keywords = Field(KeywordsNode)

    def resolve_history(self, info):
        query = History.get_query(info)
        return query.all()

    def resolve_session_account(self, info):
        return SessionAccountNode()

    def resolve_generator(self, info):
        return GeneratorNode()

    def resolve_archive(self, info):
        return ArchiveUploadStatusNode()

    def resolve_api_key(self, info):
        return KeyNode()

    def resolve_keywords(self, info):
        return KeywordsNode()


class Mutations(ObjectType):
    create_person = CreatePerson.Field()
    upload_file = UploadFile.Field()
    signup = SignUpMutation.Field()
    signin = SignInMutation.Field()
    forgot_password = ForgotMutation.Field()
    reset_password = ResetMutation.Field()
    account_update = AccountUpdateMutation.Field()
    update_password = UpdateMutation.Field()
    upload_archive = ArchiveUploadMutation.Field()
    rotate_secret = RotateSecretMutation.Field()
    update_api_key = UpdateKeyMutation.Field()
    delete_api_key = DeleteKeyMutation.Field()
    create_api_key = CreateKeyMutation.Field()
    add_keyword_ownership = AddKeywordOwnershipMutation.Field()
    add_keyword_ownership_url = AddKeywordOwnershipURLMutation.Field()
    own_keyword = OwnKeywordMutation.Field()
    own_keyword_refresh = OwnKeywordRefreshMutation.Field()
    own_keyword_revert = OwnKeywordRevertMutation.Field()
    own_keyword_reset = OwnKeywordResetMutation.Field()
    upload_keyword_ownership_csv = UploadKeywordOwnershipCSVMutation.Field()


schema = Schema(query=Query, mutation=Mutations)
