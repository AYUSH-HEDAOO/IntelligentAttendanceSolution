import uuid
from django.db import models
from core_apps.common.models import IASModel
from core_apps.users.models import Role
from core_apps.institutes.models import (
    Institute,
    Department,
    AcademicSession,
    AcademicClass,
    AcademicSection,
)


# Create your models here.
class Student(IASModel):
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=100)
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name="institute_student", null=True
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="student_department",
        null=True,
    )
    created_by_uuid_role = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.role.user.full_name} - Student"
    


class AcademicInfo(IASModel):
    """
    AcademicSession model to store Institute Session
    """

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_academic"
    )
    academic_class = models.ForeignKey(
        AcademicClass, on_delete=models.CASCADE, related_name="class_academic"
    )
    academic_section = models.ForeignKey(
        AcademicSection, on_delete=models.CASCADE, related_name="section_academic"
    )
    session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, related_name="session_academic"
    )
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name="institute_academic"
    )

    def __str__(self):
        return f"{self.student} - {self.institute.institute_name}"
