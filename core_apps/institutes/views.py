from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import (
    DepartmentForm,
    DesignationForm,
    StaffForm,
    StudentForm,
    AcademicSectionForm,
    AcademicClassForm,
    AcademicSessionForm,
)
from core_apps.common.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from core_apps.common.models import RoleType, ROLE_URL_MAP
from .models import (
    Department,
    Designation,
    AcademicSection,
    AcademicClass,
    AcademicSession,
)
from core_apps.staffs.models import Staff
from core_apps.students.models import Student


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def dashboard(request):
    return render(request, "institutes/dashboard.html")


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_department(request):
    # session_institute is the logged in user's institute
    session_institute = request.user.role_data.institute
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(session_institute)
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadDepartment"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadDepartment"))
    else:
        form = DepartmentForm()
    departments = Department.objects.filter(institute=session_institute).order_by(
        "pkid"
    )
    context = {"form": form, "departments": departments}
    return render(request, "institutes/manage_department/department.html", context)


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_designation(request):
    # session_institute is the logged in user's institute
    session_institute = request.user.role_data.institute
    if request.method == "POST":
        form = DesignationForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(session_institute)
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadDesignation"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadDesignation"))
    else:
        form = DesignationForm()
    designations = Designation.objects.filter(institute=session_institute).order_by(
        "pkid"
    )
    context = {"form": form, "designations": designations}
    return render(request, "institutes/manage_designation/designation.html", context)


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_staff(request):
    # session_institute is the logged in user's institute
    session_institute = request.user.role_data.institute
    if request.method == "POST":
        form = StaffForm(request.POST, institute=session_institute)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save()
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadStaff"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadStaff"))
    else:
        form = StaffForm(institute=session_institute)
    staffs = Staff.objects.filter(institute=session_institute).order_by("pkid")
    context = {"form": form, "staffs": staffs}
    return render(request, "institutes/manage_staff/staff.html", context)


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_student(request):
    # session_institute is the logged in user's institute
    session_institute = request.user.role_data.institute
    if request.method == "POST":
        form = StudentForm(request.POST, institute=session_institute)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save()
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadStudent"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadStudent"))
    else:
        form = StudentForm(institute=session_institute)
    students = Student.objects.filter(institute=session_institute).order_by("pkid")
    context = {"form": form, "students": students}
    return render(request, "institutes/manage_student/student.html", context)


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_academic_section(request):
    # session_institute is the logged in user's institute
    session_institute = request.user.role_data.institute
    if request.method == "POST":
        form = AcademicSectionForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(session_institute)
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadAcademicSection"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadAcademicSection"))
    else:
        form = AcademicSectionForm()
    academic_sections = AcademicSection.objects.filter(
        institute=session_institute
    ).order_by("pkid")
    context = {"form": form, "academic_sections": academic_sections}
    return render(
        request, "institutes/manage_academic_section/academic_section.html", context
    )


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_academic_class(request):
    # session_institute is the logged in user's institute
    session_institute = request.user.role_data.institute
    if request.method == "POST":
        form = AcademicClassForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(session_institute)
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadAcademicClass"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadAcademicClass"))
    else:
        form = AcademicClassForm()
    academic_classes = AcademicClass.objects.filter(
        institute=session_institute
    ).order_by("pkid")
    context = {"form": form, "academic_classes": academic_classes}
    return render(
        request, "institutes/manage_academic_class/academic_classes.html", context
    )


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_academic_session(request):
    # session_institute is the logged in user's institute
    session_institute = request.user.role_data.institute
    if request.method == "POST":
        form = AcademicSessionForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(session_institute)
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadAcademicSession"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadAcademicSession"))
    else:
        form = AcademicSessionForm()
    academic_sessions = AcademicSession.objects.filter(
        institute=session_institute
    ).order_by("pkid")
    context = {"form": form, "academic_sessions": academic_sessions}
    return render(
        request, "institutes/manage_academic_session/academic_session.html", context
    )
