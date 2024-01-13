from typing import Callable

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.module_loading import import_string

from .models import UserStatus
from .settings import graphql_auth_settings as app_settings

UserModel = get_user_model()


def get_user_by_email(email):
    """
    get user by email or by secondary email
    raise ObjectDoesNotExist
    """
    user = (
        UserModel._default_manager.select_related('status')
        .filter(Q(**{UserModel.EMAIL_FIELD: email}) | Q(status__secondary_email=email))  # type: ignore
        .first()
    )
    if user is None:
        raise ObjectDoesNotExist
    return user
    # try:
    #     user = UserModel._default_manager.select_related('status').get(**{UserModel.EMAIL_FIELD: email}) # type: ignore
    #     return user
    # except ObjectDoesNotExist:
    #     status = UserStatus._default_manager.select_related('user').get(secondary_email=email)
    #     return status.user


def get_user_to_login(**kwargs):
    """
    get user by kwargs or secondary email
    to perform login
    raise ObjectDoesNotExist
    """
    # if app_settings.ALLOW_LOGIN_WITH_SECONDARY_EMAIL:
    #     user = UserModel._default_manager.select_related('status').filter(

    #     )
    if 'email' in kwargs.keys():
        lookup_filter = Q(email=kwargs['email'])
        if app_settings.ALLOW_LOGIN_WITH_SECONDARY_EMAIL:
            lookup_filter |= Q(status__secondary_email=kwargs['email'])
        user = UserModel._default_manager.select_related('status').filter(lookup_filter).first()
    else:
        user = UserModel._default_manager.select_related('status').filter(**kwargs).first()
    if user:
        return user
    else:
        raise ObjectDoesNotExist

    # try:
    #     user = UserModel._default_manager.get(**kwargs)
    #     return user
    # except ObjectDoesNotExist:
    #     if app_settings.ALLOW_LOGIN_WITH_SECONDARY_EMAIL:
    #         email = kwargs.get(UserModel.EMAIL_FIELD, None)
    #         if email:
    #             status = UserStatus._default_manager.get(secondary_email=email)
    #             return status.user
    #     raise ObjectDoesNotExist


def get_async_email_func() -> Callable | None:
    if app_settings.is_async_email:
        return import_string(app_settings.EMAIL_ASYNC_TASK)
    return None


async_email_func = get_async_email_func()
