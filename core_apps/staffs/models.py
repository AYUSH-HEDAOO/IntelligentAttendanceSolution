from django.db import models
from core_apps.common.models import IASModel,BloodGroup, Gender
from core_apps.users.models import Role
from core_apps.institutes.models import Department, Designation,Institute

# Create your models here.
class Staff(IASModel):
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="staff_department", null=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name="staff_designation", null=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name="institute_staff",null=True)
    created_by_uuid_role = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(blank=True, default="/profile_images/default_profile.png")
    dob = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True, choices=Gender.choices, default=Gender.PREFER_NOT_TO_ANSWER)
    blood_group = models.CharField(max_length=10, null=True, blank=True, choices=BloodGroup.choices, default=BloodGroup.OTHER)
    mobile_no = models.CharField(max_length=16, null=True, blank=True)
    about = models.CharField(max_length=566, null=True, blank=True)
    
    

    def __str__(self):
        return f"{self.role.user.full_name} - Staff of {self.department.department_name} on designation {self.designation.designation_name}"