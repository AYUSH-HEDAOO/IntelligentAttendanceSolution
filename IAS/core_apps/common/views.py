import os
import pickle
import time
from datetime import date

import cv2
import imutils
import numpy as np
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from imutils import face_utils
from sklearn.preprocessing import LabelEncoder

from IAS.core_apps.attendance.filters import AttendanceFilter
from IAS.core_apps.attendance.models import Attendance
from IAS.core_apps.attendance.resources import AttendanceResource
from IAS.core_apps.common.decorators import allowed_users
from IAS.core_apps.common.models import ROLE_URL_MAP, AttendanceStatus, BloodGroup, Gender, RoleType
from IAS.core_apps.common.utils.datetime_utils import get_current_time
from IAS.core_apps.common.utils.face_detection_utils import predict, prepare_directory
from IAS.core_apps.common.utils.image_utils import CustomFaceAligner as FaceAligner
from IAS.core_apps.common.utils.image_utils import get_detector, get_predictor
from IAS.core_apps.institutes.models import Institute
from IAS.core_apps.staffs.models import Staff
from IAS.core_apps.students.models import AcademicInfo, Student
from IAS.core_apps.users.models import Role

User = get_user_model()
CAMERA_IP = settings.CAMERA_IP
BASE_DIR = settings.BASE_DIR


def mark_attendance(request):
    detector = get_detector()
    predictor = get_predictor()
    svc_save_path = f"{BASE_DIR}\\ias\\face_recognition_data\\svc.sav"

    with open(svc_save_path, "rb") as f:
        svc = pickle.load(f)
    fa = FaceAligner(predictor, desiredFaceWidth=100)
    encoder = LabelEncoder()
    encoder.classes_ = np.load(f"{BASE_DIR}\\ias\\face_recognition_data\\classes.npy")

    faces_encodings = np.zeros((1, 128))
    no_of_faces = len(svc.predict_proba(faces_encodings)[0])
    count = dict()
    present = dict()
    start = dict()
    for i in range(no_of_faces):
        user_id = encoder.inverse_transform([i])[0]
        count[user_id] = 0
        present[user_id] = False

    # Fetch images from the URL
    image_url = f"http://{CAMERA_IP}/640x480.jpg"

    iterations = 0
    while iterations < 5:
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image_array = np.asarray(bytearray(response.raw.read()), dtype=np.uint8)
                frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                frame = imutils.resize(frame, width=800)
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = detector(gray_frame, 0)

                for face in faces:
                    (x, y, w, h) = face_utils.rect_to_bb(face)
                    face_aligned = fa.align(frame, gray_frame, face)
                    (pred, prob) = predict(face_aligned, svc)

                    if pred != [-1]:
                        user_id = encoder.inverse_transform(np.ravel([pred]))[0]
                        if count[user_id] == 0:
                            start[user_id] = time.time()
                            count[user_id] += 1

                        if count[user_id] == 4 and (time.time() - start[user_id]) > 1.2:
                            count[user_id] = 0
                        else:
                            present[user_id] = True
                            count[user_id] += 1
                            print(f"Found user: {user_id}, Present: {present[user_id]}, Count: {count[user_id]}")

                    cv2.putText(
                        frame,
                        str(user_id) + str(prob),
                        (x + 6, y + h - 6),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        1,
                    )

                cv2.imshow("Mark Attendance - In - Press q to exit", frame)
                if cv2.waitKey(50) & 0xFF == ord("q"):
                    break

            else:
                print(f"Error: Failed to fetch image. Status code: {response.status_code}")
                break

        except Exception as e:
            print(f"Error: {e}")
            break

        iterations += 1
        time.sleep(1)

    cv2.destroyAllWindows()
    name = update_attendance_in_db_in(present)
    return redirect(f"/?attendance={name}")


def get_user_ids_with_true_values(input_dict):
    return [key for key, value in input_dict.items() if value]


def get_attendance_data(current_user, filter_date):
    session_institute = current_user.institute
    attendances = []
    todays_attendance = Attendance.objects.none()
    if current_user.role_type == RoleType.STUDENT:
        student = Student.objects.get(role=current_user, institute=session_institute)
        academic_info = AcademicInfo.objects.filter(student=student).order_by("pkid")
        if academic_info:
            academic_info = academic_info[0]
            attendances = Attendance.objects.filter(academic_info=academic_info,
                                                    a_date__lt=filter_date).order_by("-a_date")
            todays_attendance, _ = Attendance.objects.get_or_create(
                a_date=filter_date,
                institute=session_institute,
                academic_info=academic_info,
                academic_class_section=academic_info.academic_class_section,
                session=academic_info.session,
                a_type=RoleType.STUDENT,
            )
    elif current_user.role_type == RoleType.STAFF:
        staff = Staff.objects.get(role=current_user, institute=session_institute)
        attendances = Attendance.objects.filter(staff=staff, a_date__lt=filter_date).order_by("-a_date")
        todays_attendance, _ = Attendance.objects.get_or_create(
            a_date=filter_date,
            institute=session_institute,
            staff=staff,
            a_type=RoleType.STAFF,
        )
    return attendances, todays_attendance


def update_attendance_in_db_in(clock_in_data):
    user_ids = get_user_ids_with_true_values(clock_in_data)
    name = ""
    for user_id in user_ids:
        # Mark attendance for user_id
        user = User.objects.get(id=user_id)
        current_user = Role.objects.get(user=user)
        name = current_user.user.full_name
        print("Marking Attendance for User", current_user.user.full_name)
        _, todays_attendance = get_attendance_data(current_user, date.today())
        todays_attendance = mark_all_attendance(current_user, todays_attendance)
    return name


def create_dataset(role_data, max_sample_count=30):
    try:
        user = role_data.user
        user_id = user.id
        institute_id = role_data.institute.id
        directory = prepare_directory(institute_id, user_id)
        print("[INFO] Loading the facial detector")
        detector = get_detector()
        predictor = get_predictor()
        fa = FaceAligner(predictor, desiredFaceWidth=100)

        # URL of the image that updates frequently
        image_url = f"http://{CAMERA_IP}/640x480.jpg"

        # Our dataset naming counter
        start_sample_num = user.last_image_number

        # Capturing the faces one by one and detecting the faces
        while start_sample_num != max_sample_count:
            try:
                # Fetch the image from the URL
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    # Convert the image to a numpy array
                    image_array = np.asarray(bytearray(response.raw.read()), dtype=np.uint8)
                    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

                    # Resize the frame
                    frame = imutils.resize(frame, width=800)

                    # Convert to grayscale for face detection
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = detector(gray_frame, 0)

                    for face in faces:
                        (x, y, w, h) = face_utils.rect_to_bb(face)

                        # Align the face
                        face_aligned = fa.align(frame, gray_frame, face)

                        # Increment the sample number
                        start_sample_num += 1

                        # Save the aligned face image
                        if face_aligned is not None:
                            cv2.imwrite(
                                os.path.join(directory, f"{start_sample_num}.jpg"),
                                face_aligned,
                            )
                            face_aligned = imutils.resize(face_aligned, width=400)

                        # Draw a rectangle around the face
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

                    # Display the frame
                    cv2.imshow("Add Images", frame)

                    # Wait for a short period (50ms) and check for 'q' key press to exit
                    if cv2.waitKey(50) & 0xFF == ord("q"):
                        break

                else:
                    print(f"Error: Failed to fetch image. Status code: {response.status_code}")
                    break

            except Exception as e:
                print(f"Error fetching or processing image: {e}")
                break

        # Update the user's last image number
        user.last_image_number = start_sample_num - 1
        user.save()
        return True

    except Exception as e:
        print("Error in create_dataset:", e)
        return False

    finally:
        cv2.destroyAllWindows()


def mark_all_attendance(current_user, todays_attendance):
    with transaction.atomic():
        created_by_uuid_role = f"{current_user.user.id}/{current_user.role_type}"
        current_time = get_current_time()
        if not todays_attendance.a_in_time:
            todays_attendance.a_in_time = current_time
            todays_attendance.a_status = AttendanceStatus.PRESENT
            todays_attendance.created_by_uuid_role = created_by_uuid_role
            todays_attendance.a_type = current_user.role_type
        else:
            todays_attendance.a_out_time = current_time
            todays_attendance.a_type = current_user.role_type
            todays_attendance.a_status = AttendanceStatus.PRESENT
        todays_attendance.save()
    return todays_attendance


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.STUDENT, RoleType.OWNER, RoleType.STAFF])
def add_images_to_dataset(request):
    current_user = request.user.role_data
    status = create_dataset(current_user, max_sample_count=29)
    url_name = ROLE_URL_MAP[current_user.role_type]
    if status:
        messages.success(request, "Photos added successfully.")
    else:
        messages.error(request, "Failed to add photos.")
    return redirect(reverse(url_name))


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.STUDENT, RoleType.OWNER, RoleType.STAFF])
def profile(request):
    current_user = request.user.role_data
    if current_user.role_type == RoleType.STUDENT:
        student = Student.objects.get(role=current_user)
        if request.method == "POST":
            dob = request.POST.get("dob")
            state = request.POST.get("state", "")
            about = request.POST.get("about", "")
            gender = request.POST.get("gender", "")
            address = request.POST.get("address", "")
            blood_group = request.POST.get("blood_group", "")
            profile_image = request.FILES.get("profile_image", "")
            mobile_no = request.POST.get("mobile_no", "")

            student.dob = dob
            student.state = state
            student.about = about
            student.gender = gender
            student.address = address
            student.blood_group = blood_group
            student.profile_image = profile_image
            student.mobile_no = mobile_no
            student.save()

            messages.success(request, "Profile updated successfully.")
            return redirect(reverse("ProfileUpdateRead"))
    elif current_user.role_type == RoleType.OWNER:
        institute = Institute.objects.get(id=current_user.institute.id)
        if request.method == "POST":
            institute_name = request.POST.get("institute_name", "")
            institute_reg_number = request.POST.get("institute_reg_number", "")
            phone_number = request.POST.get("phone_number", "")
            address = request.POST.get("address", "")
            city = request.POST.get("city", "")
            institute_image = request.FILES.get("institute_image", None)

            institute.institute_name = institute_name
            institute.institute_reg_number = institute_reg_number
            institute.phone_number = phone_number
            institute.address = address
            institute.city = city
            if institute_image:
                institute.institute_image = institute_image
            institute.save()

            messages.success(request, "Profile updated successfully.")
            return redirect(reverse("ProfileUpdateRead"))
    elif current_user.role_type == RoleType.STAFF:
        staff = Staff.objects.get(role=current_user)
        if request.method == "POST":
            profile_image = request.FILES.get("profile_image", None)
            dob = request.POST.get("dob", "")
            state = request.POST.get("state", "")
            address = request.POST.get("address", "")
            gender = request.POST.get("gender", "")
            blood_group = request.POST.get("blood_group", "")
            mobile_no = request.POST.get("mobile_no", "")
            about = request.POST.get("about", "")
            if profile_image:
                staff.profile_image = profile_image
            staff.dob = dob
            staff.state = state
            staff.address = address
            staff.blood_group = blood_group
            staff.gender = gender
            staff.mobile_no = mobile_no
            staff.about = about
            staff.save()
            messages.success(request, "Profile updated successfully.")
            return redirect(reverse("ProfileUpdateRead"))

    context = {"blood_groups": BloodGroup, "genders": Gender}
    return render(request, "common/manage_profile/profile.html", context)


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER, RoleType.STAFF])
def attendance_list(request):
    # session_institute is the logged in user's institute
    current_user = request.user.role_data
    session_institute = request.user.role_data.institute
    if current_user.role_type == RoleType.STAFF:
        attendance_queryset = Attendance.objects.filter(
            institute=session_institute, is_deleted=False, a_type=RoleType.STUDENT
        )
    else:
        attendance_queryset = Attendance.objects.filter(institute=session_institute, is_deleted=False)
    attendance_filter = AttendanceFilter(request.GET, queryset=attendance_queryset)

    context = {
        "todays_attendance": attendance_filter.qs,
        "attendance_filter": attendance_filter,
    }
    return render(request, "attendance/manage_attendance/attendance.html", context)


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER, RoleType.STAFF])
def export_attendance_csv(request):
    current_user = request.user.role_data
    session_institute = request.user.role_data.institute
    if current_user.role_type == RoleType.STAFF:
        attendance_queryset = Attendance.objects.filter(
            institute=session_institute, is_deleted=False, a_type=RoleType.STUDENT
        )
    else:
        attendance_queryset = Attendance.objects.filter(institute=session_institute, is_deleted=False)
    attendance_filter = AttendanceFilter(request.GET, queryset=attendance_queryset)
    dataset = AttendanceResource().export(attendance_filter.qs)

    response = HttpResponse(dataset.csv, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="filtered_attendance.csv"'
    return response
