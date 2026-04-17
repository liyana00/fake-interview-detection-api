from django.contrib import admin
from .models import UserRegister, InterviewSession, DetectionLog

admin.site.register(UserRegister)
admin.site.register(InterviewSession)
admin.site.register(DetectionLog)