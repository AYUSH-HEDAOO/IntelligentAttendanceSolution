from ias.core_apps.common.models import IASModel, RoleType, AttendanceStatus
from django.db import models
from ias.core_apps.institutes.models import Institute
from ias.core_apps.staffs.models import Staff
from ias.core_apps.students.models import (
    AcademicInfo,
    AcademicClassSection,
    AcademicSession,
)
from django.contrib.auth import get_user_model

AUTH_USER = get_user_model()

# Create your models here.


class Attendance(IASModel):
    academic_info = models.ForeignKey(
        AcademicInfo, on_delete=models.CASCADE, related_name="academic_attendance", null=True, blank=True
    )
    academic_class_section = models.ForeignKey(
        AcademicClassSection, on_delete=models.CASCADE, related_name="class_section_attendance", null=True, blank=True
    )
    session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, related_name="session_attendance", null=True, blank=True
    )
    a_date = models.DateField()
    a_in_time = models.TimeField(blank=True, null=True)
    a_out_time = models.TimeField(blank=True, null=True)
    a_status = models.CharField(
        max_length=10,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.ABSENT,
    )
    a_type = models.CharField(
        max_length=10, choices=RoleType.choices, default=RoleType.STUDENT
    )
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name="institute_attendance", null=True, blank=True
    )
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name="staff_attendance", null=True, blank=True
    )
    created_by_uuid_role = models.TextField(null=True, blank=True)

    @property
    def created_by_name(self):
        if self.created_by_uuid_role and "/" in self.created_by_uuid_role:
            uuid, role = str(self.created_by_uuid_role).split("/")
            created_user = AUTH_USER.objects.get(id=uuid)

            return f"{created_user.first_name} {created_user.last_name} ({role})"
        return "System"

    @property
    def badge_color(self):
        if self.a_status == AttendanceStatus.PRESENT:
            return "success"
        elif self.a_status == AttendanceStatus.ABSENT:
            return "danger"
        elif self.a_status == AttendanceStatus.ON_LEAVE:
            return "warning"
        elif self.a_status == AttendanceStatus.WEEKEND:
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
        return f"{self.a_type} of {self.a_status} for date {self.a_date}"
