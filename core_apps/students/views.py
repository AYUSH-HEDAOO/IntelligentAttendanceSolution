from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from core_apps.common.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from core_apps.common.models import RoleType, ROLE_URL_MAP, AttendanceStatus, BloodGroup, Gender
from .models import Attendance, AcademicInfo, Student
from datetime import date, datetime
from django.db import transaction


def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


def get_months_map():
    """
    Returns a dictionary mapping month digits to abbreviated month names.
    """
    import calendar

    return {i: calendar.month_abbr[i] for i in range(1, 13)}


# Create your views here.
@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.STUDENT])
def dashboard(request):
    current_user = request.user.role_data
    todays_date = date.today()
    attendances, todays_attendance = get_attendance_data(current_user, todays_date)
    months_map = get_months_map()
    filter_status = request.GET.get("status")
    filter_month = request.GET.get(
        "month", date.today().strftime("%m")
    )  # Get the month from query params
    if filter_month and filter_month.isdigit():  # Validate that the month is a number
        filter_month = int(filter_month)
    present_count = attendances.filter(
        a_date__month=filter_month, a_status=AttendanceStatus.PRESENT
    ).count()
    absent_count = attendances.filter(
        a_date__month=filter_month, a_status=AttendanceStatus.ABSENT
    ).count()
    leave_count = attendances.filter(
        a_date__month=filter_month, a_status=AttendanceStatus.ON_LEAVE
    ).count()

    if request.method == "POST":
        with transaction.atomic():
            created_by_uuid_role = f"{current_user.user.id}/{current_user.role_type}"
            current_time = get_current_time()
            if not todays_attendance.a_in_time:
                todays_attendance.a_in_time = current_time
                todays_attendance.a_status = AttendanceStatus.PRESENT
                todays_attendance.created_by_uuid_role = created_by_uuid_role
            else:
                todays_attendance.a_out_time = current_time
                todays_attendance.a_status = AttendanceStatus.PRESENT
            todays_attendance.save()
            messages.success(request, "Attendance updated successfully.")
        todays_attendance = Attendance.objects.get(id=todays_attendance.id)

    context = {
        "attendances": (
            attendances.filter(a_status=filter_status) if filter_status else attendances
        ),
        "todays_attendance": todays_attendance,
        "months_map": months_map,
        "present_count": present_count,
        "absent_count": absent_count,
        "leave_count": leave_count,
        "current_month": months_map[filter_month],
        "attendance_status": AttendanceStatus,
    }
    return render(request, "students/dashboard.html", context)



@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.STUDENT])
def profile(request):
    current_user = request.user.role_data
    student = Student.objects.get(role=current_user)
    if request.method == 'POST':
        dob = request.POST.get('dob')
        state = request.POST.get('state', "")
        about = request.POST.get('about', "")
        gender = request.POST.get('gender',"")
        address = request.POST.get('address',"")
        blood_group = request.POST.get('blood_group',"")
        profile_image = request.FILES.get('profile_image', "")
        print("profile_image", profile_image)
        mobile_no = request.POST.get('mobile_no',"")

        student.dob = dob
        student.state = state
        student.about = about
        student.gender = gender
        student.address = address
        student.blood_group = blood_group
        student.profile_image = profile_image
        student.mobile_no = mobile_no
        student.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect(reverse('StudentProfileUpdateRead'))

    context = {"student": student, "blood_groups": BloodGroup, "genders": Gender}
    return render(request, "students/manage_profile/profile.html", context)



@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.STUDENT, RoleType.OWNER, RoleType.STAFF])
def attendance_create_read(request):
    current_user = request.user.role_data
    attendances, todays_attendance = get_attendance_data(current_user, filter_date=date.today())
    context = {"attendances": attendances, "todays_attendance": todays_attendance}
    return render(request, "students/manage_attendance/attendance.html", context)


def get_attendance_data(current_user, filter_date):
    session_institute = current_user.institute
    attendances = []
    todays_attendance = Attendance.objects.none()

    student = Student.objects.get(role=current_user, institute=session_institute)
    academic_info = AcademicInfo.objects.filter(student=student).order_by("pkid")
    if academic_info:
        academic_info = academic_info[0]
        attendances = Attendance.objects.filter(
            academic_info=academic_info, a_date__lt=filter_date
        ).order_by("-a_date")
        todays_attendance, is_created = Attendance.objects.get_or_create(
            a_date=filter_date,
            institute=session_institute,
            academic_info=academic_info,
            academic_class=academic_info.academic_class,
            academic_section=academic_info.academic_section,
            session=academic_info.session,
        )
    return attendances, todays_attendance
