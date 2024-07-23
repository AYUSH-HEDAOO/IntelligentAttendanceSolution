from django.db import models
from core_apps.common.models import IASModel
from core_apps.users.models import Role

# Create your models here.
class Staff(IASModel):
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.role.user.get_full_name()} - Staff"