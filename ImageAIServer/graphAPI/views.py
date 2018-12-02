from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from .ImageAI import getCoordsFromImageResnet
from rest_framework.views import APIView
import pdb
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class ImageProcessorView(APIView):
    authentication_classes = []
    def post(self, request):
        photo = request.FILES.get('photo')
        photo_path = photo.temporary_file_path()
        coords = getCoordsFromImageResnet(photo_path)
        data = {'coords': coords}
        return JsonResponse(data)


