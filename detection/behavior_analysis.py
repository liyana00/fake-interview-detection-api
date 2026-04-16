# import cv2
# import mediapipe as mp

# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh()


# def analyze_behavior(frame):
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = face_mesh.process(rgb)

#     if not results.multi_face_landmarks:
#         return "No Face"

#     for face in results.multi_face_landmarks:
#         nose = face.landmark[1]

#         h, w, _ = frame.shape
#         nose_x = int(nose.x * w)

#         center = w // 2

#         if nose_x < center - 40:
#             return "Looking Left"
#         elif nose_x > center + 40:
#             return "Looking Right"
#         else:
#             return "Focused"

#     return "Normal"
import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)


def analyze_behavior(frame):
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return "No Face"

    for face_landmarks in results.multi_face_landmarks:
        # ✅ Nose tip landmark (very important)
        nose = face_landmarks.landmark[1]

        nose_x = int(nose.x * w)

        center = w // 2

        # ✅ REAL LOGIC
        if abs(nose_x - center) < 40:
            return "Focused"  # Looking at camera

        elif nose_x < center - 40:
            return "Looking Left"

        elif nose_x > center + 40:
            return "Looking Right"

    return "Normal"