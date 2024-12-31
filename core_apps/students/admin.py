from django.contrib import admin
from .models import Student, Attendance, AcademicInfo
# Register your models here.
admin.site.register(Student)
admin.site.register(AcademicInfo)
admin.site.register(Attendance)