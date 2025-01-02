import uuid
from django.db import models
from core_apps.common.models import IASModel, AttendanceStatus
from core_apps.users.models import Role
from core_apps.institutes.models import (
    Institute,
    Department,
    AcademicSession,
    AcademicClass,
    AcademicSection,
)
from django.contrib.auth import get_user_model

AUTH_USER = get_user_model()

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
    
    @property
    def created_by_name(self):
        created_name = ""
        if self.created_by_uuid_role and "/" in self.created_by_uuid_role:
            uuid, role = str(self.created_by_uuid_role).split('/')
            created_user = AUTH_USER.objects.get(id=uuid)
            created_name = f"{created_user.first_name} {created_user.last_name} ({role})"
        return created_name
    


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

class Attendance(IASModel):
    academic_info = models.ForeignKey(
        AcademicInfo, on_delete=models.CASCADE, related_name="academic_attendance"
    )
    academic_class = models.ForeignKey(
        AcademicClass, on_delete=models.CASCADE, related_name="class_attendance"
    )
    academic_section = models.ForeignKey(
        AcademicSection, on_delete=models.CASCADE, related_name="section_attendance"
    )
    session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, related_name="session_attendance"
    )
    a_date = models.DateField()
    a_in_time = models.TimeField(blank=True,null=True)
    a_out_time = models.TimeField(blank=True, null=True)
    a_status = models.CharField(max_length=10, choices=AttendanceStatus.choices, default=AttendanceStatus.NOT_MARKED)
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name="institute_attendance"
    )
    created_by_uuid_role = models.TextField(null=True, blank=True)
    
    @property
    def created_by_name(self):
        if self.created_by_uuid_role and "/" in self.created_by_uuid_role:
            uuid, role = str(self.created_by_uuid_role).split('/')
            created_user = AUTH_USER.objects.get(id=uuid)
        
            return f"{created_user.first_name} {created_user.last_name} ({role})"
        return ""
    
    @property
    def badge_color(self):
        if self.a_status == AttendanceStatus.PRESENT:
            return "success"
        elif self.a_status == AttendanceStatus.ABSENT:
            return "danger"
        elif self.a_status == AttendanceStatus.NOT_MARKED:
            return "warning"
        elif self.a_status == AttendanceStatus.ON_LEAVE:
            return "secondary"
        else:
            return "info"
        
    @property
    def in_time(self):
        if self.a_in_time:
            return self.a_in_time.strftime("%H:%M:%S")
        return "Not Yet"
    
    @property
    def out_time(self):
        if self.a_out_time:
            return self.a_out_time.strftime("%H:%M:%S")
        return "Not Yet"
    
    def __str__(self):
        return f"{self.academic_info.student.role.user.first_name} was {self.a_status} for date {self.a_date}"
    