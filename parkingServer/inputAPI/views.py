from django.shortcuts import render

from __future__ import unicode_literals

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Image
from .serializers import ImageSerializer

# Create your views here.

class CreateView(generics.ListCreateAPIView):

    queryset = Image.objects.all()

    parser_classes = (FormParser, MultiPartParser,)
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        print(self.request.data)
        print(self.request._files)
        serializer.save()