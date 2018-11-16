from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import DetailsView
from .views import DisplayStateListView

urlpatterns = {
    url(r'^displayState/$', DisplayStateListView.get_display_state, name="details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
