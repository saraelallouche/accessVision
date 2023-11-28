from django.urls import path

from accessVisionBack.views import YoloAPIView, YoloView

urlpatterns = [
    path("yolo", YoloView.as_view(), name="yolo"),
    path("yoloApi", YoloAPIView.as_view(), name="yoloApi"),

]