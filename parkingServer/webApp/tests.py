from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from mainModels.models import Sector, SectorSpot, ImageCoordinates, LotState
from .serializer import SectorSerializer
# Create your tests here.

class ViewTests(TestCase):
    fixtures = ['../test_resources/fixtures/data.json']
    def setUp(self):
        self.client = APIClient()

    def testViewSectors(self):
        lot_id = 2

        response = self.client.get('/sectors/?parkingLot=' + str(lot_id))

        print(response)
        print(response.content)

    def testViewRows(self):
        lot_id = 1

        response = self.client.get('/rows/?parkingLot=' + str(lot_id))

        print(response)
        print(response.content)

    # def test_sector_has_sector_spots(self):
    #     print(sectorspot)

