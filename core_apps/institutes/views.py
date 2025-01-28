from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import StreamingHttpResponse
from django.contrib import messages
from django.conf import settings
from .forms import (
    DepartmentForm,
    DesignationForm,
    StaffForm,
    StudentForm,
    AcademicSectionForm,
    AcademicClassForm,
    AcademicSessionForm,
    AcademicInfoForm,
    
)
from core_apps.common.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from core_apps.common.models import RoleType, ROLE_URL_MAP, STUDENT_CRUD_URL_MAP
from .models import (
    Department,
    Designation,
    AcademicSection,
    AcademicClass,
    AcademicSession,
    
)
from core_apps.staffs.models import Staff
from core_apps.students.models import Student,AcademicInfo
import cv2 as cv
import numpy as np
import os
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from keras_facenet import FaceNet


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
    state = False
    # session_institute is the logged in user's institute
    session_institute = request.user.role_data.institute
    if request.method == "POST":
        form = StaffForm(request.POST, institute=session_institute)
        if form.is_valid():
            state = True
            # Handle form data here
            # status, _message = form.save()
            # if status:
            #     messages.success(request, f"{_message}")
            # else:
            #     messages.warning(request, f"{_message}")
            # return redirect(reverse("CreateReadStaff"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadStaff"))
    else:
        form = StaffForm(institute=session_institute)
    staffs = Staff.objects.filter(institute=session_institute).order_by("pkid")
    context = {"form": form, "staffs": staffs ,"state": state}
    return render(request, "institutes/manage_staff/staff.html", context)

def get_embedding(facenet, face_img):
    face_img = face_img.astype('float32')
    face_img = np.expand_dims(face_img, axis=0)
    yhat = facenet.embeddings(face_img)
    return yhat[0]

def video_stream(name):
    facenet = FaceNet()
    haarcascade = cv.CascadeClassifier(os.path.join(settings.BASE_DIR, 'staticfiles', 'assets', 'camassets', 'haarcascade_frontalface_default.xml'))
    count = 0

    # Check if embeddings and model files exist
    embeddings_file = "faces_embeddings_done_4classes.npz"
    model_file = "svm_model_160x160.pkl"

    if os.path.exists(embeddings_file):
        faces_embeddings = np.load(embeddings_file)
        EMBEDDED_X = faces_embeddings['arr_0']
        Y = faces_embeddings['arr_1']
    else:
        EMBEDDED_X = np.empty((0, 512))  # Assuming 512 is the embedding size
        Y = np.array([])

    if os.path.exists(model_file):
        model = pickle.load(open(model_file, 'rb'))
    else:
        model = SVC(kernel='linear', probability=True)

    encoder = LabelEncoder()
    if len(Y) > 0:
        encoder.fit(Y)


    cap = cv.VideoCapture(1)
    while cap.isOpened():
        _, frame = cap.read()
        rgb_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = haarcascade.detectMultiScale(gray_img, 1.3, 5)

        for x, y, w, h in faces:
            face = rgb_img[y:y+h, x:x+w]
            face = cv.resize(face, (160, 160))
            face_embedding = get_embedding(facenet, face)
            face_embedding = np.expand_dims(face_embedding, axis=0)
            
            if len(Y) > 0:
                decision_values = model.decision_function(face_embedding)
                confidence = np.max(decision_values)
            else:
                confidence = 0

            if confidence > 1:
                face_name = model.predict(face_embedding)
                final_name = encoder.inverse_transform(face_name)[0]
                cv.putText(frame, str(final_name), (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
            else:
                EMBEDDED_X = np.vstack([EMBEDDED_X, face_embedding])
                Y = np.append(Y, name)

                if len(np.unique(Y)) == 1:
                    dummy_embedding = np.random.rand(512)  # Random dummy embedding
                    EMBEDDED_X = np.vstack([EMBEDDED_X, dummy_embedding])
                    Y = np.append(Y, "Dummy_Class")

                # Encode the labels
                encoder.fit(Y)
                Y_encoded = encoder.transform(Y)

                # Retrain the model with the new data
                model.fit(EMBEDDED_X, Y_encoded)

                # Save the updated embeddings and model
                np.savez_compressed(os.path.join(settings.BASE_DIR, 'staticfiles', 'assets', 'camassets', embeddings_file), EMBEDDED_X, Y)
                with open(os.path.join(settings.BASE_DIR, 'staticfiles', 'assets', 'camassets', model_file), 'wb') as f:
                    pickle.dump(model, f)

                count += 1
                cv.putText(frame, "Registered", (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)

        if count > 4:
            break

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

def video_feed(request, name):
    return StreamingHttpResponse(video_stream(name),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER, RoleType.STAFF])
def create_read_student(request):
    current_user = request.user.role_data
    state = False
    # session_institute is the logged in user's institute
    session_institute = current_user.institute
    current_user_role = current_user.role_type
    redirect_url_name = STUDENT_CRUD_URL_MAP.get(current_user_role)
    if request.method == "POST":
        form = StudentForm(request.POST, current_user=current_user)
        if form.is_valid():
            state = True
        #     # Handle form data here
        #     status, _message = form.save()
        #     if status:
        #         messages.success(request, f"{_message}")
        #     else:
        #         messages.warning(request, f"{_message}")
        #     return redirect(reverse(redirect_url_name))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse(redirect_url_name))
    else:
        form = StudentForm(current_user=current_user)
    students = Student.objects.filter(institute=session_institute).order_by("pkid")
    context = {"form": form, "students": students, "state": state}
    if current_user_role == RoleType.OWNER:
        return render(request, "institutes/manage_student/student.html", context)
    else:
        return render(request, "institutes/manage_student/staff_student.html", context)
        


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


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def create_read_academic_info(request):
    # session_institute is the logged in user's institute
    session_institute = request.user.role_data.institute
    if request.method == "POST":
        form = AcademicInfoForm(request.POST, institute=session_institute)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save()
            if status:
                messages.success(request, f"{_message}")
            else:
                messages.warning(request, f"{_message}")
            return redirect(reverse("CreateReadAcademicInfo"))
        else:
            messages.warning(request, f"{form.errors}")
            return redirect(reverse("CreateReadAcademicInfo"))
    else:
        form = AcademicInfoForm(institute=session_institute)
    academic_information = AcademicInfo.objects.filter(institute=session_institute, is_deleted=False).order_by("pkid")
    context = {"form": form, "academic_info": academic_information}
    return render(request, "institutes/manage_academic_info/academic_info.html", context)


@login_required(login_url=ROLE_URL_MAP[RoleType.ANONYMOUS])
@allowed_users(allowed_roles=[RoleType.OWNER])
def delete_academic_info(request):
    if request.method == "POST":
        academic_info_id = request.POST.get("academic_info_id")
        academic_info = AcademicInfo.objects.filter(id=academic_info_id).first()
        if academic_info:
            academic_info.soft_delete()
            messages.success(request, "Academic information deleted successfully.")
        else:
            messages.warning(request, "Academic information not found.")
    return redirect(reverse("CreateReadAcademicInfo"))



