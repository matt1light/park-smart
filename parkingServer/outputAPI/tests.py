from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
import json

from mainModels.models import ArduinoOutput, ParkingLot, Output, LotState, Row, Spot


# Create your tests here.

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.request_factory = APIRequestFactory()

        self.parking_lot = ParkingLot.objects.create(description = "", name= "")
        self.arduino_output = ArduinoOutput.objects.create(parking_lot=self.parking_lot, ip_address="1234")
        self.lot_state = LotState.objects.create(parking_lot=self.parking_lot, active=True)
        self.row = Row.objects.create(lot_state=self.lot_state, active=True)
        self.spot = Spot.objects.create(row=self.row, active=True, full=False)


    def test_get_display_state_without_output(self):
        self.response = self.client.get('/displayState/')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_display_state_by_output_returns_correct_display_state(self):
        # simple display state

        # self.response = self.client.get(
        #     '/displayState/',
        #     {'output': 1})

        request = self.request_factory.get(
            '/displayState/',
            {'output': 1})

        dict_content = json.loads(self.response.content.decode('utf-8'))

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict_content["lightState"], [2])
        self.assertEqual(dict_content["signState"]["num_active_spots"], 1)
        self.assertEqual(dict_content["signState"]["num_full_spots"], 0)

