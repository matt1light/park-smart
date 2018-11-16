# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from django.utils import timezone

# Create your tests here.

class ViewTestCase(TestCase):
    def setUp(self):
        """Define the test client"""
        self.client = APIClient()

    def test_api_can_create_image(self):
        time_now = timezone.now()

        p = open('../test_resources/test_pics/test_cat.jpg', 'rb')
        data = {'time_taken': time_now, 'photo': p}

        self.response = self.client.post(
            '/image/', data=data, format='multipart'
        )

        print(self.response)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED, self.response)

    def test_api_can_create_multiple_images(self):

        time_now = timezone.now()

        p1 = open('../test_resources/test_pics/test_cat.jpg', 'rb')
        p2 = open('../test_resources/test_pics/test1.jpg', 'rb')

        data = [
            {'time_taken': time_now, 'photo': p1},
            {'time_taken': time_now, 'photo': p2}
        ]

        self.response = self.client.post(
            '/image', data=data, format='multipart'
        )

        print(self.response)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED, self.response)
