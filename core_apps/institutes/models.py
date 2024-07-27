# from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import IASModel

# Institute model
class Institute(IASModel):
    institute_name = models.CharField(max_length=200)
    institute_reg_number = models.CharField(max_length=100,null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name=_("phone number"), max_length=30, default="")
    address = models.TextField(verbose_name=_("address"), default="")
    city = models.CharField(verbose_name=_("city"), max_length=180, default="Nagpur", blank=False, null=False)
    institute_image = models.ImageField(verbose_name=_("institute image"), default="/profile_default.png")

    def __str__(self):
        return self.institute_name

    def __str__(self):
        return f"{self.institute_name}"