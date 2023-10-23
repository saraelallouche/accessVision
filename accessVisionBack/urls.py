from django.urls import path

from accessVisionBack.views import YoloAPIView

urlpatterns = [
    path("yolo", YoloAPIView.as_view(), name="yolo"),
]