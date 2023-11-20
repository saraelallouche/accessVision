from django.db import models

from accessVisionBack.model.size import Size


class Element(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=250)
    french_name = models.CharField(max_length=250, null=True, blank=True)
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.SET_NULL)
    alerte = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name