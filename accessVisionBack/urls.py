from django.urls import path
from accessVisionBack.views import YoloAPIView, YoloView, TestView

urlpatterns = [
    path("yolo", YoloView.as_view(), name="yolo"),
    path("yoloApi", YoloAPIView.as_view(), name="yoloApi"),
    path("test-backend", TestView.as_view(), name="test-backend"),

]