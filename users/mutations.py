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