from graphene import ObjectType, String, List, Mutation


class Errors(ObjectType):
    class Meta:
        name = "Errors"
    key = String()
    messages = List(String)


class GatewayObjectType(ObjectType):
    errors = List(Errors)
