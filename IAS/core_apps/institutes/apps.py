from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InstitutesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "IAS.core_apps.institutes"
    verbose_name = _("Institute")
    verbose_name_plural = _("Institutes")
