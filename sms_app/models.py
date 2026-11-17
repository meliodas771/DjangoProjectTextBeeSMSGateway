from django.db import models

class SmsHistory(models.Model):
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.status}"