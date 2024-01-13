import graphene
import graphql_jwt
from graphene.types.generic import GenericScalar
from graphql_jwt.mixins import JSONWebTokenMixin
from graphql_jwt.settings import jwt_settings

from .bases import DynamicArgsMixin, MutationMixin
from .mixins import (
    ArchiveAccountMixin,
    DeleteAccountMixin,
    ObtainJSONWebTokenMixin,
    PasswordChangeMixin,
    PasswordResetMixin,
    PasswordSetMixin,
    RegisterMixin,
    RemoveSecondaryEmailMixin,
    ResendActivationEmailMixin,
    SendPasswordResetEmailMixin,
    SendSecondaryEmailActivationMixin,
    SwapEmailsMixin,
    UpdateAccountMixin,
    VerifyAccountMixin,
    VerifyOrRefreshOrRevokeTokenMixin,
    VerifySecondaryEmailMixin,
)
from .queries import UserNode
from .settings import graphql_auth_settings as app_settings
from .types import ExpectedErrorType

# from .utils import normalize_fields, using_refresh_tokens
from .utils import using_refresh_tokens


class Register(MutationMixin, DynamicArgsMixin, RegisterMixin, graphene.Mutation):
    if app_settings.ALLOW_LOGIN_NOT_VERIFIED:
        token = graphene.Field(graphene.String)
        if using_refresh_tokens():
            refresh_token = graphene.Field(graphene.String)
    errors = graphene.Field(ExpectedErrorType)

    __doc__ = RegisterMixin.__doc__

    password_fields = [] if app_settings.ALLOW_PASSWORDLESS_REGISTRATION else ["password1", "password2"]
    # _required_args = normalize_fields(app_settings.REGISTER_MUTATION_FIELDS, password_fields)
    _required_args = app_settings.REGISTER_MUTATION_FIELDS + password_fields
    _args = app_settings.REGISTER_MUTATION_FIELDS_OPTIONAL


class VerifyAccount(MutationMixin, DynamicArgsMixin, VerifyAccountMixin, graphene.Mutation):
    __doc__ = VerifyAccountMixin.__doc__
    _required_args = ["token"]


class ResendActivationEmail(MutationMixin, DynamicArgsMixin, ResendActivationEmailMixin, graphene.Mutation):
    __doc__ = ResendActivationEmailMixin.__doc__
    _required_args = ["email"]


class SendPasswordResetEmail(MutationMixin, DynamicArgsMixin, SendPasswordResetEmailMixin, graphene.Mutation):
    __doc__ = SendPasswordResetEmailMixin.__doc__
    _required_args = ["email"]


class SendSecondaryEmailActivation(
    MutationMixin, DynamicArgsMixin, SendSecondaryEmailActivationMixin, graphene.Mutation
):
    __doc__ = SendSecondaryEmailActivationMixin.__doc__
    _required_args = ["email", "password"]


class VerifySecondaryEmail(MutationMixin, DynamicArgsMixin, VerifySecondaryEmailMixin, graphene.Mutation):
    __doc__ = VerifySecondaryEmailMixin.__doc__
    _required_args = ["token"]


class SwapEmails(MutationMixin, DynamicArgsMixin, SwapEmailsMixin, graphene.Mutation):
    __doc__ = SwapEmailsMixin.__doc__
    _required_args = ["password"]


class RemoveSecondaryEmail(MutationMixin, DynamicArgsMixin, RemoveSecondaryEmailMixin, graphene.Mutation):
    __doc__ = RemoveSecondaryEmailMixin.__doc__
    _required_args = ["password"]


class PasswordSet(MutationMixin, PasswordSetMixin, DynamicArgsMixin, graphene.Mutation):
    __doc__ = PasswordSetMixin.__doc__
    _required_args = ["token", "new_password1", "new_password2"]


class PasswordReset(MutationMixin, DynamicArgsMixin, PasswordResetMixin, graphene.Mutation):
    __doc__ = PasswordResetMixin.__doc__
    _required_args = ["token", "new_password1", "new_password2"]


class ObtainJSONWebToken(MutationMixin, ObtainJSONWebTokenMixin, graphql_jwt.JSONWebTokenMutation):
    __doc__ = ObtainJSONWebTokenMixin.__doc__
    user = graphene.Field(UserNode)
    unarchiving = graphene.Boolean(default_value=False)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update({"password": graphene.String(required=True)})
        for field in app_settings.LOGIN_ALLOWED_FIELDS:
            cls._meta.arguments.update({field: graphene.String()})
        if not jwt_settings.JWT_HIDE_TOKEN_FIELDS:
            cls._meta.fields['token'] = graphene.Field(graphene.String, required=False)
            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                cls._meta.fields['refresh_token'] = graphene.Field(graphene.String, required=False)
        return super(JSONWebTokenMixin, cls).Field(*args, **kwargs)
        # return super(graphql_jwt.JSONWebTokenMutation, cls).Field(*args, **kwargs)


class ArchiveAccount(MutationMixin, ArchiveAccountMixin, DynamicArgsMixin, graphene.Mutation):
    __doc__ = ArchiveAccountMixin.__doc__
    _required_args = ["password"]


class DeleteAccount(MutationMixin, DeleteAccountMixin, DynamicArgsMixin, graphene.Mutation):
    __doc__ = DeleteAccountMixin.__doc__
    _required_args = ["password"]


class PasswordChange(MutationMixin, PasswordChangeMixin, DynamicArgsMixin, graphene.Mutation):
    token = graphene.Field(graphene.String)
    if using_refresh_tokens():
        refresh_token = graphene.Field(graphene.String)

    __doc__ = PasswordChangeMixin.__doc__
    _required_args = ["old_password", "new_password1", "new_password2"]


class UpdateAccount(MutationMixin, DynamicArgsMixin, UpdateAccountMixin, graphene.Mutation):
    __doc__ = UpdateAccountMixin.__doc__
    _args = app_settings.UPDATE_MUTATION_FIELDS


class VerifyToken(MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Verify):
    payload = GenericScalar(required=False)

    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__


class RefreshToken(MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Refresh):
    payload = GenericScalar(required=False)

    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__

    @classmethod
    def Field(cls, *args, **kwargs):
        if not jwt_settings.JWT_HIDE_TOKEN_FIELDS:
            cls._meta.fields["token"] = graphene.Field(graphene.String, required=False)

            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                cls._meta.fields["refresh_token"] = graphene.Field(graphene.String, required=False)

        return super(JSONWebTokenMixin, cls).Field(*args, **kwargs)   # type: ignore


class RevokeToken(MutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.Revoke):
    revoked = graphene.Int(required=False)

    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__
