# from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import IASModel

# Institute model
class Institute(IASModel):
    institute_name = models.CharField(max_length=200)
    institute_reg_number = models.CharField(max_length=100,null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name=_("phone number"), max_length=30, default="", region="IN")
    address = models.TextField(verbose_name=_("address"), default="")
    city = models.CharField(verbose_name=_("city"), max_length=180, default="Nagpur", blank=False, null=False)
    institute_image = models.ImageField(verbose_name=_("institute image"), default="/profile_default.png")

    def __str__(self):
        return f"{self.institute_name}"
    

class Department(IASModel):
    """
    Department model to store Institute Departments
    """
    department_name = models.CharField(max_length=200)
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    def __str__(self):
        return f"{self.department_name} - {self.institute.institute_name}"

    @staticmethod
    def is_department_exists(department_name, institute):
        try:
            Department.objects.get(department_name=department_name, institute=institute)
            return True
        except Exception:
            return False

    def __str__(self):
        return f"{self.department_name}"
    
    
class Designation(IASModel):
    """
    Department model to store Institute Departments
    """
    designation_name = models.CharField(max_length=200)
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name="designation"
    )

    def __str__(self):
        return f"{self.designation_name} - {self.institute.institute_name}"

    @staticmethod
    def is_designation_exists(designation_name, institute):
        try:
            Designation.objects.get(designation_name=designation_name, institute=institute)
            return True
        except Exception:
            return False

    def __str__(self):
        return f"{self.designation_name}"
    

class AcademicSection(IASModel):
    """
    AcademicSection model to store Institute AcademicSection
    """
    section_name = models.CharField(max_length=200)
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name="academic_section"
    )

    def __str__(self):
        return f"{self.section_name} - {self.institute.institute_name}"

    @staticmethod
    def is_section_exists(section_name, institute):
        try:
            AcademicSection.objects.get(section_name=section_name, institute=institute)
            return True
        except Exception:
            return False

    def __str__(self):
        return f"{self.section_name}"
      


class AcademicClass(IASModel):
    """
    AcademicClass model to store Institute AcademicClass
    """
    class_name = models.CharField(max_length=200)
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name="academic_class"
    )

    def __str__(self):
        return f"{self.class_name} - {self.institute.institute_name}"

    @staticmethod
    def is_class_exists(class_name, institute):
        try:
            AcademicClass.objects.get(class_name=class_name, institute=institute)
            return True
        except Exception:
            return False

    def __str__(self):
        return f"{self.class_name}"


class AcademicSession(IASModel):
    """
    AcademicSession model to store Institute Session
    """
    session_name = models.CharField(max_length=200)
    is_current_session = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name="academic_session"
    )

    def __str__(self):
        return f"{self.session_name} - {self.institute.institute_name}"

    @staticmethod
    def is_session_exists(start_date, end_date, institute):
        try:
            AcademicSession.objects.get(start_date=start_date, end_date=end_date, institute=institute)
            return True
        except Exception:
            return False

    def __str__(self):
        return f"{self.session_name} is currently {'not' if not self.is_current_session else ''} active"
    