from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "IAS.core_apps.common"
    verbose_name = _("Common")
    verbose_name_plural = _("Commons")
