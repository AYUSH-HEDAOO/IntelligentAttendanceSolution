from django.shortcuts import render
from ias.core_apps.attendance.models import Attendance
from ias.core_apps.students.models import AcademicInfo
from ias.core_apps.staffs.models import Staff

from datetime import date
    

# Create your views here.
# TODO: Need to implement the logic
def sync_attendance(request):
    staffs = Staff.objects.filter(is_deleted=False)
    academic_info = AcademicInfo.objects.filter(is_deleted=False)
    today_date  = date.today()
    attendances = Attendance.objects.filter(date=today_date)
