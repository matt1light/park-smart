from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import DetailsView
from .views import get_display_state

urlpatterns = [
    url(r'^displayState/$', get_display_state, name="details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
