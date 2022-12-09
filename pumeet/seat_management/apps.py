from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CandidateProfileConfig(AppConfig):
    name = 'pumeet.seat_management'
    verbose_name: str = _("Seat_Management")
