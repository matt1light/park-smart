from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ImageProcessorView, ImageProcessorCalibrationView

urlpatterns = [
    url(r'^car_coordinates/$', ImageProcessorView.as_view(), name="process_photo"),
    url(r'^car_coordinates_calibrate/$', ImageProcessorCalibrationView.as_view(), name="calibrate_photo"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
