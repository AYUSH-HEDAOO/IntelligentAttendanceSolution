import os

import face_recognition
import numpy as np
from django.conf import settings

MEDIA_ROOT = settings.MEDIA_ROOT
BASE_DIR = settings.BASE_DIR
CAMERA_IP = settings.CAMERA_IP


def predict(face_aligned, svc, threshold=0.7):
    try:
        x_face_locations = face_recognition.face_locations(face_aligned)
        faces_encodings = face_recognition.face_encodings(face_aligned, known_face_locations=x_face_locations)
        if len(faces_encodings) == 0:
            return ([-1], [0])

    except Exception as e:
        print(f"Error in face recognition: {e}")
        return ([-1], [0])

    prob = svc.predict_proba(faces_encodings)
    result = np.where(prob[0] == np.amax(prob[0]))
    if prob[0][result[0]] <= threshold:
        return ([-1], prob[0][result[0]])

    return (result[0], prob[0][result[0]])


def prepare_directory(institute_id, user_id):
    directory = f"{MEDIA_ROOT}/image_dataset/{institute_id}/{user_id}/"
    os.makedirs(directory, exist_ok=True)
    return directory
