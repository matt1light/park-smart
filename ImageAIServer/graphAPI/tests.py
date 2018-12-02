from django.test import TestCase
from rest_framework.test import APIClient

# Create your tests here.

class ViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_basic_image_request(self):
        photo_path = "../test_resources/test_pics/e2esituations/e2e2.jpg"
        photo = open(photo_path, 'rb')
        response = self.client.post("/car_coordinates/", data = {'photo': photo}, format = 'multipart')

        print(response)

