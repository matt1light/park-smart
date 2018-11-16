from django.shortcuts import render
from django.views.generic import ListView
from .models import DisplayState
from django.http import JsonResponse
from rest_framework import status

# Create your views here.

class DisplayStateListView():
    @staticmethod
    def get_display_state(request):
        outputId = request.GET.get('output', None)
        if outputId is None:
            return JsonResponse({'error': 'request requires output as a parameter'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            display_state = DisplayState(outputId)
        except Exception as e:
            return JsonResponse({'error': e}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(display_state.get_dict())