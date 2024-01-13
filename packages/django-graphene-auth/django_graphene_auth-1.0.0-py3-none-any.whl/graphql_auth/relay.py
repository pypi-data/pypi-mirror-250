import graphene
import graphql_jwt
from graphene.types.generic import GenericScalar

from graphql_jwt.mixins import JSONWebTokenMixin
from graphql_jwt.settings import jwt_settings

from .bases import DynamicInputMixin, RelayMutationMixin
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

# from .utils import normalize_fields, using_refresh_tokens
from .utils import using_refresh_tokens


class Register(RelayMutationMixin, DynamicInputMixin, RegisterMixin, graphene.ClientIDMutation):
    success = graphene.Boolean(default_value=True)
    if app_settings.ALLOW_LOGIN_NOT_VERIFIED:
        token = graphene.Field(graphene.String)
        if using_refresh_tokens():
            refresh_token = graphene.Field(graphene.String)

    __doc__ = RegisterMixin.__doc__

    password_fields = [] if app_settings.ALLOW_PASSWORDLESS_REGISTRATION else ["password1", "password2"]

    # _required_inputs = normalize_fields(app_settings.REGISTER_MUTATION_FIELDS, password_fields)
    _required_inputs = app_settings.REGISTER_MUTATION_FIELDS + password_fields
    _inputs = app_settings.REGISTER_MUTATION_FIELDS_OPTIONAL


class VerifyAccount(RelayMutationMixin, DynamicInputMixin, VerifyAccountMixin, graphene.ClientIDMutation):
    __doc__ = VerifyAccountMixin.__doc__
    _required_inputs = ["token"]


class ResendActivationEmail(
    RelayMutationMixin, DynamicInputMixin, ResendActivationEmailMixin, graphene.ClientIDMutation
):
    success = graphene.Boolean(default_value=True)
    __doc__ = ResendActivationEmailMixin.__doc__
    _required_inputs = ["email"]


class SendPasswordResetEmail(
    RelayMutationMixin, DynamicInputMixin, SendPasswordResetEmailMixin, graphene.ClientIDMutation
):
    success = graphene.Boolean(default_value=True)
    __doc__ = SendPasswordResetEmailMixin.__doc__
    _required_inputs = ["email"]


class SendSecondaryEmailActivation(
    RelayMutationMixin,
    DynamicInputMixin,
    SendSecondaryEmailActivationMixin,
    graphene.ClientIDMutation,
):
    __doc__ = SendSecondaryEmailActivationMixin.__doc__
    _required_inputs = ["email", "password"]


class VerifySecondaryEmail(RelayMutationMixin, DynamicInputMixin, VerifySecondaryEmailMixin, graphene.ClientIDMutation):
    __doc__ = VerifySecondaryEmailMixin.__doc__
    _required_inputs = ["token"]


class SwapEmails(RelayMutationMixin, DynamicInputMixin, SwapEmailsMixin, graphene.ClientIDMutation):
    __doc__ = SwapEmailsMixin.__doc__
    _required_inputs = ["password"]


class RemoveSecondaryEmail(RelayMutationMixin, DynamicInputMixin, RemoveSecondaryEmailMixin, graphene.ClientIDMutation):
    success = graphene.Boolean(default_value=True)
    __doc__ = RemoveSecondaryEmailMixin.__doc__
    _required_inputs = ["password"]


class PasswordSet(RelayMutationMixin, DynamicInputMixin, PasswordSetMixin, graphene.ClientIDMutation):
    success = graphene.Boolean(default_value=True)
    __doc__ = PasswordSetMixin.__doc__
    _required_inputs = ["token", "new_password1", "new_password2"]


class PasswordReset(RelayMutationMixin, DynamicInputMixin, PasswordResetMixin, graphene.ClientIDMutation):
    success = graphene.Boolean(default_value=True)
    __doc__ = PasswordResetMixin.__doc__
    _required_inputs = ["token", "new_password1", "new_password2"]


class ObtainJSONWebToken(RelayMutationMixin, ObtainJSONWebTokenMixin, graphql_jwt.relay.JSONWebTokenMutation):
    __doc__ = ObtainJSONWebTokenMixin.__doc__
    user = graphene.Field(UserNode)
    unarchiving = graphene.Boolean(default_value=False)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments["input"]._meta.fields.update(
            {"password": graphene.InputField(graphene.String, required=True)}
        )
        for field in app_settings.LOGIN_ALLOWED_FIELDS:
            cls._meta.arguments["input"]._meta.fields.update({field: graphene.InputField(graphene.String)})
        if not jwt_settings.JWT_HIDE_TOKEN_FIELDS:
            cls._meta.fields['token'] = graphene.Field(graphene.String, required=False)
            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                cls._meta.fields['refresh_token'] = graphene.Field(graphene.String, required=False)
        return super(JSONWebTokenMixin, cls).Field(*args, **kwargs)
        # return super(graphql_jwt.relay.JSONWebTokenMutation, cls).Field(*args, **kwargs)


class ArchiveAccount(
    RelayMutationMixin,
    ArchiveAccountMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):
    __doc__ = ArchiveAccountMixin.__doc__
    _required_inputs = ["password"]


class DeleteAccount(RelayMutationMixin, DeleteAccountMixin, DynamicInputMixin, graphene.ClientIDMutation):
    __doc__ = DeleteAccountMixin.__doc__
    _required_inputs = ["password"]


class PasswordChange(RelayMutationMixin, PasswordChangeMixin, DynamicInputMixin, graphene.ClientIDMutation):
    token = graphene.Field(graphene.String)
    if using_refresh_tokens():
        refresh_token = graphene.Field(graphene.String)
    __doc__ = PasswordChangeMixin.__doc__
    _required_inputs = ["old_password", "new_password1", "new_password2"]


class UpdateAccount(RelayMutationMixin, DynamicInputMixin, UpdateAccountMixin, graphene.ClientIDMutation):
    __doc__ = UpdateAccountMixin.__doc__
    _inputs = app_settings.UPDATE_MUTATION_FIELDS


class VerifyToken(RelayMutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.relay.Verify):
    payload = GenericScalar(required=False)

    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__

    class Input:
        token = graphene.String(required=True)


class RefreshToken(RelayMutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.relay.Refresh):
    payload = GenericScalar(required=False)

    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__

    class Input(graphql_jwt.mixins.RefreshMixin.Fields): # type: ignore
        """Refresh Input"""

    @classmethod
    def Field(cls, *args, **kwargs):
        if not jwt_settings.JWT_HIDE_TOKEN_FIELDS:
            cls._meta.fields["token"] = graphene.Field(graphene.String, required=False)

            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                cls._meta.fields["refresh_token"] = graphene.Field(graphene.String, required=False)

        return super(JSONWebTokenMixin, cls).Field(*args, **kwargs) # type: ignore


class RevokeToken(RelayMutationMixin, VerifyOrRefreshOrRevokeTokenMixin, graphql_jwt.relay.Revoke):
    revoked = graphene.Int(required=False)

    __doc__ = VerifyOrRefreshOrRevokeTokenMixin.__doc__

    class Input:
        refresh_token = graphene.String(required=True)
