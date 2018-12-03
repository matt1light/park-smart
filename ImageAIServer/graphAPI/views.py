from django.http import JsonResponse
from .ImageAI import getCoordsFromImageResnet, getCoordsFromImageResnetCalibrate
from rest_framework.views import APIView

# Create your views here.
class ImageProcessorView(APIView):
    authentication_classes = []
    def post(self, request):
        photo = request.FILES.get('photo')
        photo_path = photo.temporary_file_path()
        coords = getCoordsFromImageResnet(photo_path)
        data = {'coords': coords}
        return JsonResponse(data)


# Create your views here.
class ImageProcessorCalibrationView(APIView):
    authentication_classes = []
    def post(self, request):
        photo = request.FILES.get('photo')
        photo_path = photo.temporary_file_path()
        coords = getCoordsFromImageResnetCalibrate(photo_path)
        data = {'coords': coords}
        return JsonResponse(data)
