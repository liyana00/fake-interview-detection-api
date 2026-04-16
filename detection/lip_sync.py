import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()


def analyze_lip_sync(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return "No Face"

    for face in results.multi_face_landmarks:
        top_lip = face.landmark[13]
        bottom_lip = face.landmark[14]

        gap = abs(top_lip.y - bottom_lip.y)

        if gap > 0.02:
            return "Talking"
        else:
            return "Not Talking"

    return "Unknown"