from django.shortcuts import redirect
import dlib
import os
from datetime import datetime, date
from django.contrib import messages
import pickle
import time
import numpy as np
from imutils.face_utils import FaceAligner
from imutils.video import VideoStream
from sklearn.preprocessing import LabelEncoder
import imutils
import cv2
from imutils import face_utils
import face_recognition
from django.db import transaction
from .models import AttendanceStatus, BloodGroup, Gender
from ias.core_apps.institutes.models import Institute
from ias.core_apps.users.models import Role
from ias.core_apps.students.models import Student, AcademicInfo
from ias.core_apps.staffs.models import Staff
from ias.core_apps.attendance.models import Attendance
from ias.core_apps.common.models import RoleType, ROLE_URL_MAP
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse
from ias.core_apps.common.decorators import allowed_users
from django.contrib.auth.decorators import login_required

User = get_user_model()

from django.conf import settings

BASE_DIR = settings.BASE_DIR
MEDIA_ROOT = settings.MEDIA_ROOT
# Add path to the shape predictor
SHAPE_PREDICTOR_PATH = f"{BASE_DIR}\\shape_predictor_68_face_landmarks.dat"


def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


def mark_attendance(request):

    detector = dlib.get_frontal_face_detector()

    predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
    svc_save_path = f"{BASE_DIR}\\ias\\face_recognition_data\\svc.sav"

    with open(svc_save_path, "rb") as f:
        svc = pickle.load(f)
    fa = FaceAligner(predictor, desiredFaceWidth=96)
    encoder = LabelEncoder()
    encoder.classes_ = np.load(f"{BASE_DIR}\\ias\\face_recognition_data\\classes.npy")

    faces_encodings = np.zeros((1, 128))
    no_of_faces = len(svc.predict_proba(faces_encodings)[0])
    count = dict()
    present = dict()
    start = dict()
    for i in range(no_of_faces):
        count[encoder.inverse_transform([i])[0]] = 0
        present[encoder.inverse_transform([i])[0]] = False

    vs = VideoStream(src=0).start()

    iterations = 0
    while iterations < 5:
        # while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=800)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_frame, 0)

        for face in faces:
            print("INFO : inside for loop")
            (x, y, w, h) = face_utils.rect_to_bb(face)
            face_aligned = fa.align(frame, gray_frame, face)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            (pred, prob) = predict(face_aligned, svc)

            if pred != [-1]:
                user_id = encoder.inverse_transform(np.ravel([pred]))[0]
                pred = user_id
                if count[pred] == 0:
                    start[pred] = time.time()
                    count[pred] = count.get(pred, 0) + 1

                if count[pred] == 4 and (time.time() - start[pred]) > 1.2:
                    count[pred] = 0
                else:
                    present[pred] = True
                    count[pred] = count.get(pred, 0) + 1
                    print("Found Data", pred, present[pred], count[pred])

                cv2.putText(
                    frame,
                    str(user_id) + str(prob),
                    (x + 6, y + h - 6),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1,
                )
                break

            else:
                user_id = "unknown"
                cv2.putText(
                    frame,
                    str(user_id),
                    (x + 6, y + h - 6),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1,
                )

        # Showing the image in another window
        # Creates a window with window name "Face" and with the image img
        cv2.imshow("Mark Attendance - In - Press q to exit", frame)

        # To get out of the loop
        key = cv2.waitKey(50) & 0xFF
        if key == ord("q"):
            break
        iterations += 1
        time.sleep(1)

    # Stoping the videostream
    vs.stop()

    # destroying all the windows
    cv2.destroyAllWindows()
    update_attendance_in_db_in(present)
    print(present)
    return redirect("Login")


def predict(face_aligned, svc, threshold=0.7):
    face_encodings = np.zeros((1, 128))
    try:
        x_face_locations = face_recognition.face_locations(face_aligned)
        faces_encodings = face_recognition.face_encodings(
            face_aligned, known_face_locations=x_face_locations
        )
        if len(faces_encodings) == 0:
            return ([-1], [0])

    except:

        return ([-1], [0])

    prob = svc.predict_proba(faces_encodings)
    result = np.where(prob[0] == np.amax(prob[0]))
    if prob[0][result[0]] <= threshold:
        return ([-1], prob[0][result[0]])

    return (result[0], prob[0][result[0]])


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
            attendances = Attendance.objects.filter(
                academic_info=academic_info, a_date__lt=filter_date
            ).order_by("-a_date")
            todays_attendance, is_created = Attendance.objects.get_or_create(
                a_date=filter_date,
                institute=session_institute,
                academic_info=academic_info,
                academic_class_section=academic_info.academic_class_section,
                session=academic_info.session,
                a_type=RoleType.STUDENT,
            )
    elif current_user.role_type == RoleType.STAFF:
        staff = Staff.objects.get(role=current_user, institute=session_institute)
        attendances = Attendance.objects.filter(
            staff=staff, a_date__lt=filter_date
        ).order_by("-a_date")
        todays_attendance, is_created = Attendance.objects.get_or_create(
            a_date=filter_date, institute=session_institute, staff=staff, a_type=RoleType.STAFF
        )
    return attendances, todays_attendance


def update_attendance_in_db_in(clock_in_data):
    user_ids = get_user_ids_with_true_values(clock_in_data)
    for user_id in user_ids:
        # Mark attendance for user_id
        user = User.objects.get(id=user_id)
        current_user = Role.objects.get(user=user)
        print("Marking Attendance for User", current_user.user.full_name)
        _, todays_attendance = get_attendance_data(current_user, date.today())
        todays_attendance = mark_all_attendance(current_user, todays_attendance)
    return True


def create_dataset(role_data, max_sample_count=30):
    try:
        id = role_data.user.id
        institute_id = role_data.institute.id
        directory = f"{MEDIA_ROOT}/image_dataset/{institute_id}/{id}/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Detect face
        # Loading the HOG face detector and the shape predictpr for allignment

        # print("[INFO] Loading the facial detector")
        detector = dlib.get_frontal_face_detector()

        predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
        fa = FaceAligner(predictor, desiredFaceWidth=96)
        # capture images from the webcam and process and detect the face
        # Initialize the video stream
        # print("[INFO] Initializing Video stream")
        vs = VideoStream(src=0).start()
        # time.sleep(2.0) ####CHECK######

        # Our identifier
        # We will put the id here and we will store the id with a face, so that later we can identify whose face it is

        # Our dataset naming counter
        sampleNum = 0
        # Capturing the faces one by one and detect the faces and showing it on the window
        while True:
            # Capturing the image
            # vs.read each frame
            frame = vs.read()
            # Resize each image
            frame = imutils.resize(frame, width=800)
            # the returned img is a colored image but for the classifier to work we need a greyscale image
            # to convert
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # To store the faces
            # This will detect all the images in the current frame, and it will return the coordinates of the faces
            # Takes in image and some other parameter for accurate result
            faces = detector(gray_frame, 0)
            # In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.

            for face in faces:
                # print("inside for loop")
                (x, y, w, h) = face_utils.rect_to_bb(face)

                face_aligned = fa.align(frame, gray_frame, face)
                # Whenever the program captures the face, we will write that is a folder
                # Before capturing the face, we need to tell the script whose face it is
                # For that we will need an identifier, here we call it id
                # So now we captured a face, we need to write it in a file
                sampleNum = sampleNum + 1
                # Saving the image dataset, but only the face part, cropping the rest

                if face is None:
                    print("face is none")
                    continue

                cv2.imwrite(directory + "/" + str(sampleNum) + ".jpg", face_aligned)
                face_aligned = imutils.resize(face_aligned, width=400)
                # cv2.imshow("Image Captured",face_aligned)
                # @params the initial point of the rectangle will be x,y and
                # @params end point will be x+width and y+height
                # @params along with color of the rectangle
                # @params thickness of the rectangle
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                # Before continuing to the next loop, I want to give it a little pause
                # waitKey of 100 millisecond
                cv2.waitKey(50)

            # Showing the image in another window
            # Creates a window with window name "Face" and with the image img
            cv2.imshow("Add Images", frame)
            # Before closing it we need to give a wait command, otherwise the open cv wont work
            # @params with the millisecond of delay 1
            cv2.waitKey(1)
            # To get out of the loop
            if sampleNum > max_sample_count:
                break

        # Stoping the videostream
        vs.stop()
        # destroying all the windows
        cv2.destroyAllWindows()
        return True
    except Exception as e:
        print("Error", e)
        return False


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
@allowed_users(allowed_roles=[RoleType.STUDENT])
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
    elif current_user.role_type == RoleType.STAFF:
        staff = Staff.objects.get(role=current_user)

    context = {"blood_groups": BloodGroup, "genders": Gender}
    return render(request, "common/manage_profile/profile.html", context)