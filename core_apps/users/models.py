import uuid
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from core_apps.common.models import IASModel
from core_apps.institutes.models import Institute

class User(AbstractBaseUser,PermissionsMixin):
    # pseudo primary key to avoid disadvantage of uuid primary key
    pkid = models.BigAutoField(primary_key=True,editable=False) 
    id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    first_name = models.CharField(verbose_name=_("first name"),max_length=50)
    last_name = models.CharField(verbose_name=_("last name"),max_length=50)
    email = models.EmailField(verbose_name=_("email address"),db_index=True,unique=True) # db_index to create indexing for email field
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["first_name","last_name"]

    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return f"{self.first_name}"
    
    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}" 
    
    @property
    def get_short_name(self):
        return self.first_name

# Role model
class Role(IASModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE,related_name="institute")
    role_type = models.CharField(max_length=10, choices=[('owner', 'Owner'), ('staff', 'Staff'), ('student', 'Student')])

    class Meta:
        unique_together = ('user', 'institute', 'role_type')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role_type}"