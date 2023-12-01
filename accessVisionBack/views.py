# Create your views here.
import json
import base64
from PIL import Image
from io import BytesIO
import os
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

class TestView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.body)
        return HttpResponse("Réponse de la route test-backend.")

class YoloAPIView(APIView):

    def post(self,request, *args, **kwargs):
        data = request.data.get('imageData')
        image_number = request.data.get('timestamp')

        # Convertir la base64 en image
        img_data = base64.b64decode(data.split(',')[1])
        image = Image.open(BytesIO(img_data))
        image_number_str = str(image_number)

        image_path = 'accessVisionBack/images/imageTest'+image_number_str+'.jpg'
        image.save(image_path)

        #os.remove(image_path)


        # Load a pretrained YOLOv8n model
        model = YOLO('yolov8n.pt')
        # Run inference on an image
        try:
            results = model(image_path)  # results list
            # View results
            for r in results:
                class_names = r.names
                boxes = r.boxes
                for box in boxes:
                    xyxy = box.xyxyn
                    cls = box.cls
                    class_name = class_names.get(int(cls.item()), 'Unknown')
                    is_center(xyxy[0], class_name)

            os.remove(image_path)

            return HttpResponse('ok')
        except Exception as e:
            return HttpResponse(e)



