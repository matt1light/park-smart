from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SectorListView
from graphene_django.views import GraphQLView
from .schema import schema
from django.views.decorators.csrf import csrf_exempt



urlpatterns = {
    # url(r'^image/$', CreateView.as_view(), name="create"),
    url(r'^sectors/$', SectorListView.as_view(), name="list_sectors"),
    url(r'^row/$', SectorListView.as_view(), name="list_sectors"),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))
}
