from django.db import models


class Size(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=250)
    size = models.FloatField()
    def __str__(self):
        return self.name
