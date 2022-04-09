import jwt
import graphene
from django.conf import settings
from django.contrib.auth import authenticate
from .models import User


class CreateAccountMutation(graphene.Mutation):

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, email, password, first_name=None, last_name=None):
        try:
            User.objects.get(email=email)
            return CreateAccountMutation(ok=False, error="User already exist")
        except User.DoesNotExist:
            try:
                User.objects.create_user(email, email, password)
                return CreateAccountMutation(ok=True)
            except Exception:
                return CreateAccountMutation(error="Can't create user")


class LoginMutation(graphene.Mutation):
    
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    error = graphene.String()
    token = graphene.String()
    pk = graphene.Int()

    def mutate(self, info, email, password):
        user = authenticate(username=email, password=password)
        if user:
            token = jwt.encode({'pk': user.pk}, settings.SECRET_KEY, algorithm='HS256')
            return LoginMutation(token=token, pk=user.pk)
        else:
            return LoginMutation(error="Wrong username or password")


class EditProfileMutation(graphene.Mutation):
    
    class Arguments:
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, email=None, first_name=None, last_name=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You need to be logged in")
        if email is not None and email != user.email:
            try:
                User.objects.get(email=email)
                return EditProfileMutation(ok=False, error="That email is taken")
            except User.DoesNotExist:
                user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.save()
        return EditProfileMutation(ok=True)
        