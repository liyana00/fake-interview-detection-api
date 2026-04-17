from django.db import models

class InterviewSession(models.Model):
    user = models.ForeignKey("UserRegister", on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.id} - {self.user.email}"


class DetectionLog(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    face_count = models.IntegerField()
    behavior = models.CharField(max_length=100)
    lip_status = models.CharField(max_length=50)

    score = models.FloatField()
    final_status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.timestamp} - {self.final_status}"

class UserRegister(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email
    
