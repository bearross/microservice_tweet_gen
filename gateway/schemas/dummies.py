from graphene_sqlalchemy import SQLAlchemyObjectType
from models.gateway import HistoryModel
from settings import datetime_format
from graphene import String, Mutation, Boolean, Field, Int, ObjectType
from graphene_file_upload.scalars import Upload
import base64
import zipfile
from mimetypes import guess_type, guess_extension


class History(SQLAlchemyObjectType):
    class Meta:
        model = HistoryModel

    created_at = String()

    def resolve_created_at(self, info):
        return str(self.created_at.strftime(datetime_format))


class Person(ObjectType):
    name = String()
    age = Int()


class CreatePerson(Mutation):
    class Arguments:
        name = String()

    ok = Boolean()
    person = Field(lambda: Person)

    @staticmethod
    def mutate(root, info, name):
        person = Person(name=name, age=35)
        ok = True
        return CreatePerson(person=person, ok=ok)


class UploadFile(Mutation):
    class Arguments:
        file = Upload()

    ok = Boolean()

    def mutate(self, info, file):
        file = file.split(",")
        file[0] = file[0]+","
        file_type = guess_extension(guess_type(file[0])[0])
        file = base64.b64decode(file[1])
        with open("files/test.zip", "wb") as w_file:
            w_file.write(file)

        try:
            if file_type != ".zip":
                raise zipfile.BadZipfile("Wrong header")
            with zipfile.ZipFile("files/test.zip") as test:
                ret = test.testzip()

                if ret is not None:
                    raise zipfile.BadZipfile("File is not a zip file")
        except zipfile.BadZipfile:
            return UploadFile(ok=False)
        return UploadFile(ok=True)
