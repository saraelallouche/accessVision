# Create your views here.
from subprocess import run

from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView

from accessVisionBack.yolo.yolov8_segmentation import ObjectDetection


class YoloAPIView(APIView):
    def get(self, *args, **kwargs):
        detector = ObjectDetection(capture_index=0)
        detector()
        return HttpResponse()



