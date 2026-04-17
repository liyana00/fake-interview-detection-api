import cv2
import mediapipe as mp

from .behavior_analysis import analyze_behavior
from .lip_sync import analyze_lip_sync
from .suspicious import calculate_suspicious_score
from .decision_engine import update_history, make_decision
from .models import InterviewSession, DetectionLog, UserRegister

running = False


def start_camera():
    global running

    # ❗ Prevent multiple camera threads
    if running:
        print("Camera already running")
        return

    running = True

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # ✅ Reduce lag
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 20)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # ✅ Warmup
    for _ in range(5):
        cap.read()

    # ✅ MediaPipe
    mp_face = mp.solutions.face_detection
    face_detection = mp_face.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.5
    )

    # ===============================
    # ✅ CREATE SESSION (ONLY ONCE)
    # ===============================
    user = UserRegister.objects.first()

    if not user:
        print("❌ No user found. Register first.")
        running = False
        return

    session = InterviewSession.objects.create(user=user)

    # ===============================

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        # ✅ Resize (faster)
        frame = cv2.resize(frame, (480, 360))

        # Mirror view
        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb)

        face_count = len(results.detections) if results.detections else 0

        # 🔍 AI Modules
        behavior = analyze_behavior(frame)
        lip = analyze_lip_sync(frame)

        # 📊 Score
        score, _ = calculate_suspicious_score(face_count, behavior, lip)

        # 🧠 Decision
        update_history(face_count, behavior, lip)
        final_status = make_decision(score)

        # ===============================
        # ✅ SAVE TO DATABASE (EVERY FRAME)
        # ===============================
        DetectionLog.objects.create(
            session=session,
            face_count=face_count,
            behavior=behavior,
            lip_status=lip,
            score=score,
            final_status=final_status
        )
        # ===============================

        # ===============================
        # ✅ UI DISPLAY
        # ===============================
        cv2.rectangle(frame, (5, 5), (420, 190), (0, 0, 0), -1)

        cv2.putText(frame, f"Faces: {face_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.putText(frame, f"Behavior: {behavior}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.putText(frame, f"Lip: {lip}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

        cv2.putText(frame, f"Score: {score}", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # 🎯 Final color
        if final_status == "Normal":
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        cv2.putText(frame, f"FINAL: {final_status}", (10, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)
        # ===============================

        cv2.imshow("Interview Monitoring", frame)

        # 🖨️ Terminal output
        print(f"Faces: {face_count} | Behavior: {behavior} | Lip: {lip} | Score: {score} | Final: {final_status}")

        # ✅ Quit with Q
        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            print("Camera stopped by Q")
            break

    # ✅ Cleanup
    cap.release()
    cv2.destroyAllWindows()
    running = False


def stop_camera():
    global running
    running = False