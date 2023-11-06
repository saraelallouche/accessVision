from django.db import models

from accessVisionBack.model.size import Size


class Element(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=250)
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name