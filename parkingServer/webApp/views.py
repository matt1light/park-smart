from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from rest_framework import generics, viewsets
from mainModels.models import Sector, ParkingLot, LotState, Row
from .serializer import SectorSerializer, RowSerializer
from rest_framework.exceptions import NotFound
from rest_framework import status

# Create your views here.
class SectorListView(generics.ListAPIView):

    serializer_class = SectorSerializer

    def get_queryset(self):
        # start with all displaystate objects
        queryset = Sector.objects.all()
        # get the desired outputId from the query parameters
        parkingLotId = self.request.query_params.get('parkingLot', None)
        # if the output Id is not none
        if parkingLotId is not None:
            try:
                # lot = ParkingLot.objects.filter(pk = parkingLotId).first()
                lotstate = LotState.objects.filter(parking_lot_id=parkingLotId).first()
                queryset = queryset.filter(lot_state = lotstate)
            except Exception as e:
                raise NotFound(detail=e)

        if not queryset:
            raise NotFound(detail={"error": "resource was not found"})
        return queryset

class RowListView(generics.ListAPIView):
    serializer_class = RowSerializer

    def get_queryset(self):
        # start with all displaystate objects
        queryset = Row.objects.all()
        # get the desired outputId from the query parameters
        parkingLotId = self.request.query_params.get('parkingLot', None)
        # if the output Id is not none
        if parkingLotId is not None:
            try:
                # lot = ParkingLot.objects.filter(pk = parkingLotId).first()
                lotstate = LotState.objects.filter(parking_lot_id=parkingLotId).first()
                queryset = queryset.filter(lot_state = lotstate)
            except Exception as e:
                raise NotFound(detail=e)

        if not queryset:
            raise NotFound(detail={"error": "resource was not found"})
        return queryset
