from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "IAS.core_apps.users"
    verbose_name = _("User")
    verbose_name_plural = _("Users")
