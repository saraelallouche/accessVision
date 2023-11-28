# Create your views here.
import json
from subprocess import run

from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView
from ultralytics import YOLO

from accessVisionBack.yolo.yolo_image import is_center
from accessVisionBack.yolo.yolov8_segmentation import ObjectDetection


class YoloView(APIView):
    def get(self, *args, **kwargs):
        detector = ObjectDetection(capture_index=0)
        detector()
        return HttpResponse()


class YoloAPIView(APIView):

    def post(self,request, *args, **kwargs):

        # Load a pretrained YOLOv8n model
        model = YOLO('yolov8n.pt')
        # Run inference on an image
        try:
            results = model("static/image/IMG_1423-2.jpg")  # results list
            # View results
            for r in results:
                class_names = r.names
                boxes = r.boxes
                for box in boxes:
                    xyxy = box.xyxyn
                    cls = box.cls
                    class_name = class_names.get(int(cls.item()), 'Unknown')
                    is_center(xyxy[0], class_name)

            return HttpResponse('ok')
        except Exception as e:
            return HttpResponse(e)



