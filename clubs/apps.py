from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClubsConfig(AppConfig):
    name = 'clubs'
    verbose_name = _('Clubs')
