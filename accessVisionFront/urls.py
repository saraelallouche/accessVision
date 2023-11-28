from django.urls import path

from accessVisionFront.views import HomeView
from accessVisionFront.views.send_video import SendVideoView
from accessVisionFront.views.video import VideoView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("home", HomeView.as_view(), name="home"),
    path("send", SendVideoView.as_view(), name="send"),
]