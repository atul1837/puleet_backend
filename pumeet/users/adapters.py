import logging
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_username
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def get_login_redirect_url(self, request: HttpRequest):
        # Create token and add frontend URL
        # Check if user exists on V1, if yes, then redirect user to v1 and delete account on v2
        user_email = request.user.email
        logger.info(
            "AccountAdapter: Returning login redirect url to [%s]" % (user_email)
        )
        token, _ = Token.objects.get_or_create(user=request.user)
        key = token.key

        # TODO: Track user logged in

        # Logout from session and continue to Webapp
        logout(request)
        return f"{settings.WEBAPP_URL}/signin?token={key}&success=true"

    def populate_username(self, request, user):
        """Set email as username"""
        email = user_email(user)
        user_username(user, email)
        user.username = email


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
