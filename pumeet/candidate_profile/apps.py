from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CandidateProfileConfig(AppConfig):
    name = 'pumeet.candidate_profile'
    verbose_name: str = _("Candidate_Profile")
