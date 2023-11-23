from django.urls import path

from accessVisionBack.views import YoloAPIView
from accessVisionBack.views import TestView


urlpatterns = [
    path("yolo", YoloAPIView.as_view(), name="yolo"),
    path("test-backend", TestView.as_view(), name="test-backend"),

]