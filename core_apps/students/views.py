from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from core_apps.common.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from core_apps.common.models import RoleType, ROLE_URL_MAP
from .forms import AttendanceForm
from .models import Attendance, AcademicInfo, Student
from datetime import date

# Create your views here.
@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.STUDENT])
def dashboard(request):
    current_user = request.user.role_data
    session_institute = current_user.institute
    student = Student.objects.get(role=current_user,institute=session_institute)
    academic_info = AcademicInfo.objects.filter(student=student).order_by("pkid")[0]
    attendances = Attendance.objects.filter(academic_info=academic_info, a_date__lte=date.today()).order_by("-a_date")
    context  = {"attendances": attendances}
    return render(request, "students/dashboard.html", context)

@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.STUDENT, RoleType.OWNER, RoleType.STAFF])
def attendance_create_read(request):
    current_user = request.user.role_data
    # session_institute is the logged in user's institute
    session_institute = current_user.institute
    if request.method == "POST":
        form = AttendanceForm(request.POST, current_user=current_user)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save()
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("StudentAttendanceCreateRead"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("StudentAttendanceCreateRead"))
    else:
        form = AttendanceForm(current_user=current_user)
    current_user = request.user.role_data
    student = Student.objects.get(role=current_user,institute=session_institute)
    academic_info = AcademicInfo.objects.filter(student=student).order_by("pkid")[0]
    attendances = Attendance.objects.filter(academic_info=academic_info, a_date__lte=date.today()).order_by("-a_date")
    context  = {"attendances": attendances, "form": form}
    return render(request, "students/manage_attendance/attendance.html", context)
