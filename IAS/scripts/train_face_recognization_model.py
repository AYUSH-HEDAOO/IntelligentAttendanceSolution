import os
import pickle

import cv2
import django
import face_recognition
import numpy as np
from django.conf import settings
from face_recognition.face_recognition_cli import image_files_in_folder
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

# Set up Django settings if not will 'raise AppRegistryNotReady("Apps aren't loaded yet.")'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IAS.ias.settings")
django.setup()

BASR_DIR = settings.BASE_DIR
MEDIA_ROOT = settings.MEDIA_ROOT


def start_training(institute) -> bool:
    print(f"Training Started for {institute.institute_name}.")
    training_dir = f"{MEDIA_ROOT}\\image_dataset\\{institute.id}"
    if not os.path.exists(training_dir):
        print(f"Training Directory not found for {institute.institute_name}")
        print("Please upload images from any Student, Staff and Institute Login.\n")
        return False

    count = 0
    for user_id in os.listdir(training_dir):
        curr_directory = os.path.join(training_dir, user_id)
        if not os.path.isdir(curr_directory):
            continue
        for _ in image_files_in_folder(curr_directory):
            count += 1

    X = []
    y = []
    i = 0
    for user_id in os.listdir(training_dir):
        curr_directory = os.path.join(training_dir, user_id)
        if not os.path.isdir(curr_directory):
            continue
        for imagefile in image_files_in_folder(curr_directory):
            image = cv2.imread(imagefile)
            try:
                X.append((face_recognition.face_encodings(image)[0]).tolist())

                y.append(user_id)
                i += 1
            except Exception as e:
                print(f"Error in image {imagefile}: {e}")
                print("removed")
                os.remove(imagefile)

    encoder = LabelEncoder()
    encoder.fit(y)
    y = encoder.transform(y)
    X1 = np.array(X)

    trained_data_path = f"{BASR_DIR}\\IAS\\face_recognition_data"
    if not os.path.exists(trained_data_path):
        os.mkdir(trained_data_path)
    np.save(f"{trained_data_path}\\classes.npy", encoder.classes_)
    svc = SVC(kernel="linear", probability=True)
    svc.fit(X1, y)

    svc_save_path = f"{trained_data_path}\\svc.sav"
    with open(svc_save_path, "wb") as f:
        pickle.dump(svc, f)
    print(f"Training Completed for {institute.institute_name}.")
    return True


if __name__ == "__main__":
    from IAS.core_apps.institutes.models import Institute
    institutes = Institute.objects.filter(is_deleted=False)
    for institute in institutes:
        result = start_training(institute)
        if result:
            print(f"Training Completed for {institute.institute_name}.")
        else:
            print(f"Training Failed for {institute.institute_name}.")
