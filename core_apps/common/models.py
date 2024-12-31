import uuid
from django.db import models


# This model is abstract model which will be inherit by other models across all the core apps
class IASModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class RoleType(models.TextChoices):
    OWNER = "owner", "Owner"
    STAFF = "staff", "Staff"
    STUDENT = "student", "Student"
    ANONYMOUS = "anonymous", "Anonymous"


ROLE_URL_MAP = {
    RoleType.OWNER: "InstituteDashboard",
    RoleType.STAFF: "StaffDashboard",
    RoleType.STUDENT: "StudentDashboard",
    RoleType.ANONYMOUS: "Login",
}

STUDENT_CRUD_URL_MAP = {
    RoleType.OWNER: "CreateReadStudent",
    RoleType.STAFF: "StaffCreateReadStudent"
}

class AttendanceStatus(models.TextChoices):
    PRESENT = "present", "Present"
    ABSENT = "absent", "Absent"
    ON_LEAVE = "on leave", "On Leave"
    NOT_MARKED = "not marked", "Not Marked"
    HOLIDAY = "holiday", "Holiday"
    weekend = "weekend", "Weekend"