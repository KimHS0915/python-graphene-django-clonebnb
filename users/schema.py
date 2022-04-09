import graphene
from .models import User
from .types import UserType
from .mutations import CreateAccountMutation, EditProfileMutation, LoginMutation
from .queries import resolve_user, resolve_me


class Query(object):

    user = graphene.Field(UserType, id=graphene.Int(required=True), resolver=resolve_user)
    me = graphene.Field(UserType, resolver=resolve_me)


class Mutation(object):

    create_account = CreateAccountMutation.Field()
    login = LoginMutation.Field()
    edit_profile = EditProfileMutation.Field()
