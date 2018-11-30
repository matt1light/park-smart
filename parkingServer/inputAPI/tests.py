# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mainModels.models import ParkingLot, LotState, Sector, Image

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.test.client import encode_multipart
import base64

from django.utils import timezone

# Create your tests here.

class ViewTestCase(TestCase):
    # def loadImage(self, path):
    #     with open(path, "rb") as imageFile:
    #         bytes = imageFile.read()
    #         base64_bytes = base64.b64encode(bytes)
    #         base64_string = base64_bytes.decode()
    #         return base64_string

    def setUp(self):
        """Define the test client"""
        self.client = APIClient()


    # def test_api_returns_400_on_failed_image(self):
    #     self.api_create_2_images()
    #     self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST, self.response)
    #     self.assertEqual(self.response.content.decode("utf-8"), '["One or more images failed validation"]')

    def test_api_can_create_image(self):
        ## set up database for successful test
        self.parking_lot = ParkingLot.objects.create(description = "", name= "")
        self.lot_state = LotState.objects.create(parking_lot=self.parking_lot, active=True)
        self.sector = Sector.objects.create(lot_state=self.lot_state, x_index=0, y_index=0, cameraID="1.1")

        #call the create image helper
        self.api_create_an_image()

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED, self.response)
        self.assertIsNotNone(self.sector.images.first())
        self.assertEqual(len(Image.objects.all()), 1)

    # helper method

    def build_input_request(self, photo, cameraID):
        time_now = timezone.now()

        p = open(photo, 'rb')

        data = {
            "cameraID": cameraID,
            "photo": p,
            "time_taken": str(time_now)
        }

        return data

    def api_create_an_image(self):
        photo = "../test_resources/test_pics/test1.jpg"
        cameraID = "1.1"

        data = self.build_input_request(photo, cameraID)

        self.response = self.client.post(
            "/image/", data=data, format="multipart"
        )


    # def api_create_2_images(self):
    #     time_now = timezone.now()
    #     p1 = open('../test_resources/test_pics/test1.jpg', 'rb')
    #     p2 = open('../test_resources/test_pics/test2.jpg', 'rb')
    #     data = {
    #         "images": [
    #             {
    #                 "cameraID": 1,
    #                 "photo": "test1.jpg",
    #                 "time_taken": str(time_now)
    #             },
    #             {
    #
    #                 "cameraID": 2,
    #                 "photo": "test2.jpg",
    #                 "time_taken": str(time_now)
    #             }
    #         ],
    #         "test1.jpg": p1,
    #         "test2.jpg": p2
    #     }
    #
    #     self.response = self.client.post(
    #         "/image-collection/", data=data, format="multipart"
    #     )
    #
    #     print(self.response)


    # def test_api_can_create_image(self):
    #     time_now = timezone.now()
    #
    #     p = open('../test_resources/test_pics/test_cat.jpg', 'rb')
    #     data = {'time_taken': time_now, 'photo': p}
    #
    #     self.response = self.client.post(
    #         '/image/', data=data, format='multipart'
    #     )
    #
    #     print(self.response)
    #     self.assertEqual(self.response.status_code, status.HTTP_201_CREATED, self.response)
    #
    # def test_api_can_create_multiple_images(self):
    #
    #     time_now = timezone.now()
    #
    #     p1 = open('../test_resources/test_pics/test_cat.jpg', 'rb')
    #     p2 = open('../test_resources/test_pics/test1.jpg', 'rb')
    #
    #     data = [
    #         {'time_taken': time_now, 'photo': p1},
    #         {'time_taken': time_now, 'photo': p2}
    #     ]
    #
    #     self.response = self.client.post(
    #         '/image', data=data, format='multipart'
    #     )
    #
    #     print(self.response)
    #     self.assertEqual(self.response.status_code, status.HTTP_201_CREATED, self.response)


    def buildRequest(hubImages):
        imgData = []

        # Create a JSON object out of each image in hubImages
        for img in hubImages:
            # Expected order of JSON elements: camera ID, photo object, timestamp
            obj = {"photoID": img.photoID, "photo": img.photo, "time": img.time}
            imgData.append(obj)

        builtRequest = json.dumps(imgData)
        return builtRequest

