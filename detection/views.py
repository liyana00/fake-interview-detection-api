from django.http import HttpResponse, JsonResponse
from .models import UserRegister
import json
import threading
from .camera import start_camera, stop_camera, running
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password

camera_running = False


def home(request):
    return HttpResponse("Backend Running ✅")


def test_api(request):
    return HttpResponse("Test API Working")


# ✅ START CAMERA
def start_detection(request):
    global running

    if running:
        return HttpResponse("Camera already running ⚠️")

    thread = threading.Thread(target=start_camera)
    thread.daemon = True
    thread.start()

    return HttpResponse("Camera started ✅")


# ✅ STOP CAMERA
def stop_detection(request):
    global camera_running
    stop_camera()
    camera_running = False
    return HttpResponse("Camera stopped")


# ✅ REGISTER
@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        data = json.loads(request.body)

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return JsonResponse({
                "status": "error",
                "message": "All fields required"
            }, status=400)

        if UserRegister.objects.filter(email=email).exists():
            return JsonResponse({
                "status": "error",
                "message": "Email already exists"
            }, status=409)

        UserRegister.objects.create(
            name=name,
            email=email,
            password=make_password(password)
        )

        return JsonResponse({
            "status": "success",
            "message": "User registered successfully"
        }, status=201)

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)


# ✅ LOGIN
@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({
                "status": "error",
                "message": "Email and password required"
            }, status=400)

        try:
            user = UserRegister.objects.get(email=email)

            if check_password(password, user.password):
                return JsonResponse({
                    "status": "success",
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email
                    }
                })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid password"
                })

        except UserRegister.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "User not found"
            })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })