# Create your views here.
from subprocess import run

from django.http import HttpResponse
from rest_framework.views import APIView


class YoloAPIView(APIView):
    def get(self, *args, **kwargs):
        result = run(['python', 'yolov8_segmentation.py'], capture_output=True, text=True)
        return HttpResponse()

class TestView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.body)
        return HttpResponse("Réponse de la route test-backend.")

