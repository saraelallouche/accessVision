from django.db import models


class Tracking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    ip = models.GenericIPAddressField()
    tracking = models.TextField()
    def __str__(self):
        return self.ip