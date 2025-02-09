from django.contrib import admin
from .models import Student, AcademicInfo

# Register your models here.
admin.site.register(Student)
admin.site.register(AcademicInfo)
