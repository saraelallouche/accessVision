# Create your views here.
import io
import json
import base64
import zipfile

import numpy as np
from PIL import Image
from io import BytesIO
import os
from subprocess import run
from datetime import datetime
from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView
from ultralytics import YOLO

from accessVisionBack.yolo.yolo_image import operation
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

    def post(self, request, *args, **kwargs):
        data = request.data.get('imageData')
        image_number = request.data.get('timestamp')
        timestamp_readable = datetime.utcfromtimestamp(int(image_number) / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

        print(f"Heure d'envoi de l'image : {timestamp_readable}")

        # Convertir la base64 en image
        img_data = base64.b64decode(data.split(',')[1])
        image = Image.open(BytesIO(img_data))
        image_number_str = str(image_number)

        image_path = 'static/image/imageTest' + image_number_str + '.jpg'
        image.save(image_path)
        print("image saved")
        # Load a pretrained YOLOv8n model
        model = YOLO('best.pt')
        audio = []
        # Run inference on an image
        try:
            results = model.track(image_path, persist=True)
            if "HTTP_X_FORWARDED_FOR" in request.META:
                ip_address = request.META["HTTP_X_FORWARDED_FOR"].split(",")[0]
            else:
                ip_address = request.META["REMOTE_ADDR"]
            # View results
            for r in results:
                class_names = r.names
                boxes = r.boxes
                for box in boxes:
                    xyxy = box.xyxyn
                    cls = box.cls
                    class_name = class_names.get(int(cls.item()), 'Unknown')
                    id = None
                    if box.id is not None:
                        id = int(box.id.item())
                    confidence = float(box.conf.item())
                    if confidence > 0.7:
                        result = operation(xyxy[0], class_name, id, ip_address)
                        if result is not None:
                            audio.append(result)

            os.remove(image_path)
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
                for index, mp3_path in enumerate(audio):
                    with open(mp3_path, 'rb') as mp3_file:
                        mp3_data = mp3_file.read()
                        zip_file.writestr(f'new_audio_{index + 1}.wav', mp3_data)

            # Set the zip file as the content of the response
            response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')

            # Set headers for downloading the zip file
            response['Content-Disposition'] = 'attachment; filename="audio_files.zip"'

            return response
        except Exception as e:
            print(e)
            return HttpResponse(e)
