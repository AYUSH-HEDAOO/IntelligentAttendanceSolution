from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import DepartmentForm,DesignationForm,StaffForm,StudentForm,AcademicClassForm,AcademicSectionForm
from core_apps.common.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from core_apps.common.models import RoleType, ROLE_URL_MAP
from .models import Department,Designation,AcademicSection,AcademicClass
from core_apps.staffs.models import Staff
from core_apps.students.models import Student


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def dashboard(request):
    return render(request, "institutes/dashboard.html")


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(request.user.role_data.institute)
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
    departments = Department.objects.filter(institute=request.user.role_data.institute)
    context = {"form": form, "departments": departments}
    return render(request, "institutes/manage_department/department.html", context)

@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_designation(request):
    if request.method == "POST":
        form = DesignationForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(request.user.role_data.institute)
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
    designations = Designation.objects.filter(institute=request.user.role_data.institute)
    context = {"form": form, "designation":designations }
    return render(request, "institutes/manage_designation/designation.html", context)


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_staff(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(request.user.role_data.institute)
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadStaff"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadStaff"))
    else:
        form = StaffForm()
    staffs = Staff.objects.filter(institute=request.user.role_data.institute)
    context = {"form": form, "staffs":staffs }
    return render(request, "institutes/manage_staff/staff.html", context)


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(request.user.role_data.institute)
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadStudent"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadStudent"))
    else:
        form = StudentForm()
    students = Student.objects.filter(institute=request.user.role_data.institute)
    context = {"form": form, "students":students }
    return render(request, "institutes/manage_student/student.html", context)


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_academicSection(request):
    if request.method == "POST":
        form = AcademicSectionForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(request.user.role_data.institute)
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadAcademicClass"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadAcademicClass"))
    else:
        form = AcademicSectionForm()
    academicSections = AcademicSection.objects.filter(institute=request.user.role_data.institute)
    context = {"form": form, "academicSection":academicSections }
    return render(request, "institutes/manage_academicSection/academicSection.html", context)



@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_academicClass(request):
    if request.method == "POST":
        form = AcademicClassForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save(request.user.role_data.institute)
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
    academicClasses = AcademicClass.objects.filter(institute=request.user.role_data.institute)
    context = {"form": form, "academicClass":academicClasses }
    return render(request, "institutes/manage_academicClass/academicClass.html", context)
