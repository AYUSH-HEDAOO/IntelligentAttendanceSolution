from django.db import models
from core_apps.common.models import IASModel
from core_apps.users.models import Role
from core_apps.institutes.models import Department, Designation,Institute

# Create your models here.
class Staff(IASModel):
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="staff_department", null=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name="staff_designation", null=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name="institute_staff",null=True)
    

    def __str__(self):
        return f"{self.role.user.full_name} - Staff of {self.department.department_name} on designation {self.designation.designation_name}"