from django.contrib import admin
from .models import Institute, Department, AcademicSession, AcademicClassSection

# Register your models here.
admin.site.register(Institute)
admin.site.register(Department)
admin.site.register(AcademicSession)
admin.site.register(AcademicClassSection)