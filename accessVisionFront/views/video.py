import requests
from django.views.generic import TemplateView

class VideoView(TemplateView):
    template_name = "camera.html"
    def get_context_data(self, **kwargs):
        url = "http://10.31.51.3:8000/back/yolo"
        response = requests.get(url).content.decode("utf-8")