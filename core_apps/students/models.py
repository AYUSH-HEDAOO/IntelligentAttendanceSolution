from django.db import models
from core_apps.common.models import IASModel
from core_apps.users.models import Role
from core_apps.institutes.models import Institute, Department

# Create your models here.
class Student(IASModel):
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=100)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name="institute_student",null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="student_department", null=True)
    
    

    def __str__(self):
        return f"{self.role.user.full_name} - Student"