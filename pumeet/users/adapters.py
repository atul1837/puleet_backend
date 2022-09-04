from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_username
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_username(self, request, user):
        """Set email as username"""
        email = user_email(user)
        user_username(user, email)
        user.username = email


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
